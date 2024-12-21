from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import DPI
from .serializers import DPISerializer
from .permissions import IsPatient , IsInfirmier , IsMedecin , IsMedecinOrInfirmier


@api_view(['POST'])
@permission_classes([IsMedecin])
def creer_dpi(request):
    """
    Crée un nouveau DPI pour un patient. Le champ `patient_id` doit être inclus dans la requête.
    """
    if request.method == 'POST':
        # Ici, on prend directement les données de la requête, y compris le champ `patient_id`
        serializer = DPISerializer(data=request.data)
        
        if serializer.is_valid():
            # Si les données sont valides, on crée le DPI
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        # Si les données ne sont pas valides, on renvoie les erreurs
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsPatient])
def consulter_dpi(request):
    """
    Consulter le DPI de l'utilisateur connecté via le token d'authentification.
    Le token d'authentification permet d'identifier l'utilisateur connecté et de récupérer son DPI.
    """
    try:
        # Récupérer le DPI pour l'utilisateur connecté en utilisant son ID via le token (request.user.id)
        dpi = DPI.objects.get(patient_id=request.user.id)
    except DPI.DoesNotExist:
        # Si aucun DPI n'est trouvé pour l'utilisateur, retourner une erreur
        return Response({'detail': 'DPI non trouvé pour cet utilisateur.'}, status=status.HTTP_404_NOT_FOUND)

    # Sérialisation et renvoi des données du DPI
    serializer = DPISerializer(dpi)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsMedecinOrInfirmier])
def rechercher_dpi_par_nss(request, nss):
    """
    Rechercher un DPI par NSS.
    Accessible uniquement aux infirmiers et medecins.
    """
    try:
        # Chercher le DPI en fonction du NSS sans filtrer par utilisateur connecté
        dpi = DPI.objects.get(nss=nss)
    except DPI.DoesNotExist:
        return Response({'detail': 'DPI non trouvé avec ce NSS.'}, status=status.HTTP_404_NOT_FOUND)

    # Sérialiser et retourner les données du DPI
    serializer = DPISerializer(dpi)
    return Response(serializer.data)


""" à revoir"""
@api_view(['GET'])
@permission_classes([IsMedecinOrInfirmier])
def consulter_dpi_par_qr(request, qr_code):
    """
    Consulter le DPI d'un patient via un QR Code (QR Code supposé contenir le NSS).
    Accessible uniquement aux infirmiers et medecins.
    """
    try:
        # Chercher le DPI en fonction du QR code (supposé être un NSS)
        dpi = DPI.objects.get(nss=qr_code)
    except DPI.DoesNotExist:
        return Response({'detail': 'DPI non trouvé avec ce QR code.'}, status=status.HTTP_404_NOT_FOUND)

    # Sérialiser et retourner les données du DPI
    serializer = DPISerializer(dpi)
    return Response(serializer.data)

