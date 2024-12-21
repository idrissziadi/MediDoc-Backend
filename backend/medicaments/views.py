from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Medicament
from .serializers import MedicamentSerializer

@api_view(['POST'])
def creer_medicament(request):
    """
    Créer un nouveau médicament.
    """
    serializer = MedicamentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def supprimer_medicament(request, id_medicament):
    """
    Supprimer un médicament par son ID.
    """
    try:
        medicament = Medicament.objects.get(id_medicament=id_medicament)
        medicament.delete()
        return Response({"detail": "Médicament supprimé avec succès."}, status=status.HTTP_204_NO_CONTENT)
    except Medicament.DoesNotExist:
        return Response({"detail": "Médicament introuvable."}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def obtenir_medicaments(request):
    """
    Récupérer la liste de tous les médicaments.
    """
    medicaments = Medicament.objects.all()
    serializer = MedicamentSerializer(medicaments, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
