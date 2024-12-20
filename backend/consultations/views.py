from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Consultation
from .serializers import ConsultationSerializer
from .permissions import IsMedecin

@api_view(['GET'])
@permission_classes([IsMedecin])
def get_all_consultations(request):
    """
    Récupérer toutes les consultations.
    Accessible uniquement aux médecins.
    """
    consultations = Consultation.objects.all()
    serializer = ConsultationSerializer(consultations, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsMedecin])
def get_consultation_by_id(request, id_consultation):
    """
    Récupérer une consultation par son ID.
    Accessible uniquement aux médecins.
    """
    try:
        consultation = Consultation.objects.get(id_consultation=id_consultation)
    except Consultation.DoesNotExist:
        return Response({'detail': 'Consultation non trouvée.'}, status=status.HTTP_404_NOT_FOUND)

    serializer = ConsultationSerializer(consultation)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsMedecin])
def create_consultation(request):
    """
    Créer une nouvelle consultation.
    Accessible uniquement aux médecins.
    """
    medecin_id = request.user.id

    data = request.data.copy()
    data['medecin'] = medecin_id


    serializer = ConsultationSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsMedecin])
def update_consultation(request, id_consultation):
    """
    Mettre à jour une consultation existante par son ID.
    Accessible uniquement aux médecins.
    """
    try:
        consultation = Consultation.objects.get(id_consultation=id_consultation)
    except Consultation.DoesNotExist:
        return Response({'detail': 'Consultation non trouvée.'}, status=status.HTTP_404_NOT_FOUND)

    serializer = ConsultationSerializer(consultation, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsMedecin])
def delete_consultation(request, id_consultation):
    """
    Supprimer une consultation par son ID.
    Accessible uniquement aux médecins.
    """
    try:
        consultation = Consultation.objects.get(id_consultation=id_consultation)
    except Consultation.DoesNotExist:
        return Response({'detail': 'Consultation non trouvée.'}, status=status.HTTP_404_NOT_FOUND)

    consultation.delete()
    return Response({'detail': 'Consultation supprimée avec succès.'}, status=status.HTTP_204_NO_CONTENT)
