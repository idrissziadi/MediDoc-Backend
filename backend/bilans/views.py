from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import  ImageRadiologique, AnalyseBiologique
from DPI.models import DPI
from .serializers import ImageRadiologiqueSerializer, AnalyseBiologiqueSerializer
from DPI.permissions import IsPatientOrMedecin

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