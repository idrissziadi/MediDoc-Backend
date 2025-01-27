from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import  ImageRadiologique, AnalyseBiologique
from DPI.models import DPI
from .serializers import ImageRadiologiqueSerializer, AnalyseBiologiqueSerializer,CustomImageRadiologiqueSerializer
from DPI.permissions import IsPatientOrMedecinOrInfirmierOrRadiologue
from .serializers import ImageRadiologiqueSerializer, AnalyseBiologiqueSerializer
from DPI.permissions import IsPatientOrMedecin
from .permissions import IsRadiologue, IsLaborantin
from .serializers import ImageRadiologiqueUpdateSerializer
from django.shortcuts import get_object_or_404
from .serializers import AnalyseBiologiqueUpdateSerializer
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

@swagger_auto_schema(
    method='get',
    manual_parameters=[
        openapi.Parameter('nss', openapi.IN_QUERY, description="Numéro de sécurité sociale (NSS) du patient", type=openapi.TYPE_STRING, required=True),
        openapi.Parameter('date', openapi.IN_QUERY, description="Filtrer les images après cette date (format YYYY-MM-DD)", type=openapi.TYPE_STRING, required=False)
    ],
    responses={200: ImageRadiologiqueSerializer(many=True), 400: "Le champ NSS est obligatoire.", 404: "DPI non trouvé"}
)
@api_view(['GET'])
@permission_classes([IsPatientOrMedecinOrInfirmierOrRadiologue])
def get_images_radiologiques(request):
    """
    Récupère les images radiologiques d'un patient (NSS requis).
    """
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


@swagger_auto_schema(
    method='get',
    manual_parameters=[
        openapi.Parameter('nss', openapi.IN_QUERY, description="Numéro de sécurité sociale (NSS) du patient", type=openapi.TYPE_STRING, required=True),
        openapi.Parameter('date', openapi.IN_QUERY, description="Filtrer les analyses après cette date (format YYYY-MM-DD)", type=openapi.TYPE_STRING, required=False)
    ],
    responses={200: AnalyseBiologiqueSerializer(many=True), 400: "Le champ NSS est obligatoire.", 404: "DPI non trouvé"}
)
@api_view(['GET'])
@permission_classes([IsPatientOrMedecinOrInfirmierOrRadiologue])
def get_analyses_biologiques(request):
    """
    Récupère les analyses biologiques d'un patient (NSS requis).
    """
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

@swagger_auto_schema(
    method='get',
    responses={200: CustomImageRadiologiqueSerializer(many=True)}
)
@api_view(['GET'])
@permission_classes([IsPatientOrMedecinOrInfirmierOrRadiologue])
def getRadiologueImages(request):
    """
    Récupère toutes les images radiologiques disponibles pour un radiologue.
    """
    user_id = request.user.id
    images = ImageRadiologique.objects.all()
    serializer = CustomImageRadiologiqueSerializer(images, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@swagger_auto_schema(
    method='get',
    responses={200: AnalyseBiologiqueSerializer(many=True)}
)
@api_view(['GET'])
@permission_classes([IsLaborantin])
def getAllAnalysesBiologiques(request):
    """
    Récupère toutes les analyses biologiques disponibles pour un laborantin.
    """
    user_id = request.user.id
    analyses = AnalyseBiologique.objects.all()
    serializer = AnalyseBiologiqueSerializer(analyses, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method='put',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['id_image_radiologique', 'url', 'compte_rendu'],
        properties={
            'id_image_radiologique': openapi.Schema(type=openapi.TYPE_INTEGER, description="ID de l'image radiologique"),
            'url': openapi.Schema(type=openapi.TYPE_STRING, description="URL de l'image radiologique"),
            'compte_rendu': openapi.Schema(type=openapi.TYPE_STRING, description="Compte rendu du radiologue"),
        },
    ),
    responses={200: ImageRadiologiqueUpdateSerializer, 404: "Image radiologique introuvable", 400: "Données invalides"}
)
@api_view(['PUT'])
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
    
@swagger_auto_schema(
    method='put',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['id_analyse_biologique', 'parametres'],
        properties={
            'id_analyse_biologique': openapi.Schema(type=openapi.TYPE_INTEGER, description="ID de l'analyse biologique"),
            'parametres': openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Items(type=openapi.TYPE_OBJECT, properties={
                    'parametre': openapi.Schema(type=openapi.TYPE_STRING, description="Nom du paramètre d'analyse"),
                    'valeur': openapi.Schema(type=openapi.TYPE_STRING, description="Valeur du paramètre d'analyse")
                })
            )
        },
    ),
    responses={200: AnalyseBiologiqueUpdateSerializer, 400: "Données invalides", 404: "Analyse biologique introuvable"}
)
@api_view(['PUT'])
@permission_classes([IsLaborantin])  # Vérifie si l'utilisateur est authentifié
def remplir_analyse_biologique(request):
    """
    Endpoint permettant à un laborantin de compléter les informations d'une analyse biologique.
    """     
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