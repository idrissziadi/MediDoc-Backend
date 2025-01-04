
from datetime import datetime
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Consultation
from bilans.models import AnalyseBiologique, ImageRadiologique
from ordonnance.models import Ordonnance
from ordonnace_has_medicament.models import OrdonnanceHasMedicament
from medicaments.models import Medicament
from .serializers import ConsultationSerializer, ConsultationDetailSerializer
from .permissions import IsMedecin,IsPatientOrMedecin

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




@api_view(['POST'])
@permission_classes([IsMedecin])
def creerConsultationAvecOrdonnance(request):
    
    medecin_id = request.user.id  # Récupérer l'ID du médecin à partir du token
    data = request.data.copy()

    try:
        # 1. Créer la consultation
        consultation_data = {
            "date": datetime.now().strftime('%Y-%m-%d'),
            "resume": data.get("resume"),
            "dpi": data.get("dpi"),
            "medecin": medecin_id
        }
        consultation_serializer = ConsultationSerializer(data=consultation_data)
        if not consultation_serializer.is_valid():
            return Response(consultation_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        consultation = consultation_serializer.save()

        # 2. Créer l'ordonnance (une seule ordonnance ici)
        ordonnance_data = data.get("ordonnance", {})  # Notez qu'il s'agit désormais d'un dictionnaire, pas d'une liste
        ordonnance = Ordonnance.objects.create(
            consultation=consultation,
            status=ordonnance_data.get("status", "non_valide")
        )

        # 3. Associer les médicaments à l'ordonnance
        medicaments_data = ordonnance_data.get("medicaments", [])
        for medicament_data in medicaments_data:
            medicament = Medicament.objects.filter(id_medicament=medicament_data.get("id_medicament")).first()
            if not medicament:
                return Response(
                    {"detail": f"Médicament avec ID {medicament_data.get('id_medicament')} non trouvé."},
                    status=status.HTTP_404_NOT_FOUND
                )

            OrdonnanceHasMedicament.objects.create(
                ordonnance=ordonnance,
                medicament=medicament,
                dose=medicament_data.get("dose"),
                duree=medicament_data.get("duree"),
                frequence=medicament_data.get("frequence")
            )

        return Response(consultation_serializer.data, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({"detail": f"Une erreur s'est produite: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['POST'])
@permission_classes([IsMedecin])
def creerConsultationAvecBilan(request):
    """
    Créer une consultation et demander des bilans (analyses biologiques et/ou images radiologiques).
    Accessible uniquement aux médecins.
    """
    medecin_id = request.user.id  # Récupérer l'ID du médecin depuis le token
    data = request.data.copy()

    try:
        # 1. Créer la consultation
        consultation_data = {
            "date": datetime.now().strftime('%Y-%m-%d'),
            "resume": data.get("resume"),
            "dpi": data.get("dpi"),
            "medecin": medecin_id
        }
        consultation_serializer = ConsultationSerializer(data=consultation_data)
        if not consultation_serializer.is_valid():
            return Response(consultation_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        consultation = consultation_serializer.save()

        # 2. Créer les demandes d'analyses biologiques
        analyses_data = data.get("analyses_biologiques", [])
        for analyse_data in analyses_data:
            AnalyseBiologique.objects.create(
                type=analyse_data.get("type"),
                consultation=consultation
            )

        # 3. Créer les demandes d'images radiologiques
        images_data = data.get("images_radiologiques", [])
        for image_data in images_data:
            ImageRadiologique.objects.create(
                type=image_data.get("type"),
                consultation=consultation
            )

        return Response(consultation_serializer.data, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({"detail": f"Une erreur s'est produite: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 

@api_view(['GET'])
@permission_classes([IsPatientOrMedecin])
def getConsultationByPatient(request, id_dpi):
    """
    Récupérer toutes les consultations d'un patient par son ID.
    Accessible aux médecins et aux patients.
    """
    try:
        # Retrieve all consultations for the given patient ID (dpi_id)
        consultations = Consultation.objects.filter(dpi_id=id_dpi)
        if not consultations.exists():
            return Response({'detail': 'Aucune consultation trouvée pour ce patient.'}, status=status.HTTP_404_NOT_FOUND)
        
        # Use ConsultationDetailSerializer if detailed information is required, otherwise ConsultationSerializer
        
        # Serialize the data for the response
        serializer = ConsultationDetailSerializer(consultations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({"detail": f"Une erreur s'est produite: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)