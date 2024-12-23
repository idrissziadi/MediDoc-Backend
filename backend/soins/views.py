from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import Soin
from DPI.models import DPI
from .serializers import SoinSerializer
from .permissions import IsInfirmier
from datetime import datetime



@api_view(['GET'])
@permission_classes([IsInfirmier])
def get_soins_par_dpi(request, dpi_id):
    """
    Récupérer tous les soins pour un DPI spécifique, en utilisant l'ID du DPI.
    Accessible uniquement aux infirmiers.
    """
    try:
        dpi = DPI.objects.get(nss=dpi_id)  # Récupérer le DPI par son ID (int)
    except DPI.DoesNotExist:
        return Response({'detail': 'DPI spécifié introuvable.'}, status=status.HTTP_404_NOT_FOUND)
    
    soins = Soin.objects.filter(dpi=dpi)  # Récupérer tous les soins associés au DPI
    serializer = SoinSerializer(soins, many=True)  # Sérialiser les soins
    return Response(serializer.data, status=status.HTTP_200_OK)



@api_view(['POST'])
@permission_classes([IsInfirmier])
def ajouterSoins(request):
    """
    Ajouter un soin pour un DPI.
    Accessible uniquement aux infirmiers.
    """
    if request.method == 'POST':
        # Ajouter l'infirmier connecté dans les données de la requête
        data = request.data.copy()
        data['infirmier'] = request.user.id  # Utilisateur connecté de type infirmier
        data['date'] = datetime.now().strftime('%Y-%m-%d')
        # Valider que le DPI existe
        dpi_id = data.get('dpi', None)
        if not DPI.objects.filter(nss=dpi_id).exists():
            return Response({'detail': 'DPI spécifié introuvable.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Sérialisation et création
        serializer = SoinSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsInfirmier])
def supprimerSoin(request, soin_id):
    """
    Supprimer un soin.
    Accessible uniquement aux infirmiers.
    """
    try:
        soin = Soin.objects.get(id_soin=soin_id)
    except Soin.DoesNotExist:
        return Response({'detail': 'Soin introuvable.'}, status=status.HTTP_404_NOT_FOUND)
    
    # Supprimer le soin
    soin.delete()
    return Response({'detail': 'Soin supprimé avec succès.'}, status=status.HTTP_204_NO_CONTENT)