from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import  ImageRadiologique, AnalyseBiologique
from DPI.models import DPI
from .serializers import ImageRadiologiqueSerializer, AnalyseBiologiqueSerializer
from DPI.permissions import IsPatientOrMedecin
from .permissions import IsRadiologue, IsLaborantin
from .serializers import ImageRadiologiqueUpdateSerializer
from django.shortcuts import get_object_or_404
from .serializers import AnalyseBiologiqueUpdateSerializer


@api_view(['GET'])
@permission_classes([IsPatientOrMedecin])
def get_images_radiologiques(request):
    nss = request.query_params.get('nss')
    date = request.query_params.get('date')

    if not nss:
        return Response({'detail': 'Le champ NSS est obligatoire.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Récupérer le DPI
        dpi = DPI.objects.get(nss=nss)
    except DPI.DoesNotExist:
        return Response({'detail': 'DPI non trouvé avec ce NSS.'}, status=status.HTTP_404_NOT_FOUND)

    # Filtrer les images radiologiques par DPI et éventuellement par date de consultation
    images = ImageRadiologique.objects.filter(consultation__dpi=dpi).select_related('consultation')

    if date:
        images = images.filter(consultation__date__gt=date)

    # Sérialiser les données
    serializer = ImageRadiologiqueSerializer(images, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsPatientOrMedecin])
def get_analyses_biologiques(request):
    nss = request.query_params.get('nss')
    date = request.query_params.get('date')

    if not nss:
        return Response({'detail': 'Le champ NSS est obligatoire.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Récupérer le DPI
        dpi = DPI.objects.get(nss=nss)
    except DPI.DoesNotExist:
        return Response({'detail': 'DPI non trouvé avec ce NSS.'}, status=status.HTTP_404_NOT_FOUND)

    # Filtrer les analyses biologiques par DPI et éventuellement par date de consultation
    analyses = AnalyseBiologique.objects.filter(consultation__dpi=dpi).select_related('consultation')

    if date:
        analyses = analyses.filter(consultation__date__gt=date)

    # Sérialiser les données
    serializer = AnalyseBiologiqueSerializer(analyses, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PATCH'])
@permission_classes([IsRadiologue])
def remplir_image_radiologique(request):
    """
    Endpoint permettant à un radiologue de compléter les informations d'une image radiologique.
    """
    data = request.data

    try:
        # Récupérer l'ID de l'image radiologique
        image_id = data.get('id_image_radiologique')
        # Vérifier si l'image existe
        try:
            image = ImageRadiologique.objects.get(id_image_radiologique=image_id)
        except ImageRadiologique.DoesNotExist:
            return Response({"detail": "Image radiologique introuvable."}, status=status.HTTP_404_NOT_FOUND)
        # Mettre à jour les champs manquants
        serializer = ImageRadiologiqueUpdateSerializer(image, data={
            "url": data.get("url"),
            "compte_rendu": data.get("compte_rendu"),
            "radiologue": request.user.id,
            "statut": "terminé"
        }, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({"detail": f"Une erreur s'est produite : {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['PATCH'])
@permission_classes([IsLaborantin])  # Vérifie si l'utilisateur est authentifié
def remplir_analyse_biologique(request):
     
    data = request.data

    try:
        # Récupérer l'ID de l'analyse biologique
        analyse_id = data.get('id_analyse_biologique')
        if not analyse_id:
            return Response({"detail": "L'ID de l'analyse biologique est obligatoire."}, status=status.HTTP_400_BAD_REQUEST)

        # Vérifier si l'analyse existe
        analyse = get_object_or_404(AnalyseBiologique, id_analyse_biologique=analyse_id)

        # Récupérer les paramètres et valeurs envoyés
        parametres = data.get("parametres", [])

        if not parametres:
            return Response({"detail": "Les paramètres sont obligatoires."}, status=status.HTTP_400_BAD_REQUEST)

        # Convertir les paramètres et valeurs en chaînes séparées par '#'
        parametre_analyse = '#'.join([item['parametre'] for item in parametres])
        valeur = '#'.join([str(item['valeur']) for item in parametres])

        # Mettre à jour l'analyse biologique
        serializer = AnalyseBiologiqueUpdateSerializer(analyse, data={
            "parametre_analyse": parametre_analyse,
            "valeur": valeur,
            "laborantin": request.user.id,  # Extraire l'ID du laborantin depuis le token utilisateur
            "statut": "terminé"  # Changer le statut à "terminé"
        }, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({"detail": f"Une erreur s'est produite : {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)    