from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import DPI
from .serializers import DPISerializer
from .serializers import DPIDetailSerializer
from .permissions import IsMedecin , IsMedecinOrInfirmier, IsAdministratifOrMedecin, IsPatientOrMedecin, IsPatient
from django.contrib.auth import get_user_model
from accounts.serializers import UserSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

@swagger_auto_schema(
    method='post',
    operation_description="Créer un DPI pour un patient. Accessible uniquement aux administratifs et médecins.",
    request_body=DPISerializer,
    responses={
        201: "DPI créé avec succès.",
        400: "Erreur lors de la création du DPI ou si le numéro de sécurité sociale existe déjà.",
        404: "Médecin spécifié introuvable.",
    }
)
@api_view(['POST'])
@permission_classes([IsAdministratifOrMedecin])
def creer_dpi(request):
            
        data = request.data.copy()   
        User = get_user_model()
        nss = data.get("nss")
        if DPI.objects.filter(nss=nss).exists():
         return Response({"detail": f"Le numéro de sécurité sociale '{nss}' existe déjà."},status=status.HTTP_400_BAD_REQUEST)
                
        medecin_nom = data.get("medecin_traitant")
        if medecin_nom:
            medecin = User.objects.filter(role="medecin", nom=medecin_nom).first()
            if not medecin:
                return Response(
                    {"detail": f"Le médecin '{medecin_nom}' n'existe pas ou n'est pas valide."},
                    status=status.HTTP_404_NOT_FOUND,
                )
            data["medecin_traitant"] = medecin.id

        # Étape 1 : Créer le patient dans la table User
        patient_data = {
            "nom": data.get("patient_nom"),
            "email": data.get("patient_email"),
            "role": "patient",  
            "password": data.get("patient_password"),
            "specialite": "other",
        }

        # Sérialiser les données du patient
        patient_serializer = UserSerializer(data=patient_data)
        if patient_serializer.is_valid():
            patient = patient_serializer.save()  # Crée le patient et récupère l'instance
            data["patient"] = patient.id  # Ajouter l'ID du patient aux données du DPI
        else:
            return Response(
                {"detail": "Erreur lors de la création du patient.", "errors": patient_serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
        # Étape 2 : Créer le DPI
        serializer = DPISerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    method='get',
    operation_description="Récupérer les informations détaillées d'un DPI en utilisant le NSS. Accessible aux patients et médecins.",
    manual_parameters=[
        openapi.Parameter('nss', openapi.IN_PATH, description="Numéro de Sécurité Sociale du patient", type=openapi.TYPE_STRING, required=True)
    ],
    responses={
        200: DPIDetailSerializer,
        404: "DPI non trouvé pour cet utilisateur."
    }
)
@api_view(['GET'])
@permission_classes([IsPatientOrMedecin])
def consulter_dpi(request, nss):
    try:
        # Récupérer le DPI pour l'utilisateur connecté en utilisant son ID via le token (request.user.id)
        dpi = DPI.objects.all().get(nss=nss)
    except DPI.DoesNotExist:
        # Si aucun DPI n'est trouvé pour l'utilisateur, retourner une erreur
        return Response({'detail': 'DPI non trouvé pour cet utilisateur.'}, status=status.HTTP_404_NOT_FOUND)
    # Sérialisation et renvoi des données détaillées du DPI
    serializer = DPIDetailSerializer(dpi)
    return Response(serializer.data, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method='get',
    operation_description="Rechercher un DPI par le NSS. Accessible uniquement aux médecins et infirmiers.",
    manual_parameters=[
        openapi.Parameter('nss', openapi.IN_PATH, description="Numéro de Sécurité Sociale du patient", type=openapi.TYPE_STRING, required=True)
    ],
    responses={
        200: "Nom du patient",
        404: "DPI non trouvé avec ce NSS."
    }
)
@api_view(['GET'])
@permission_classes([IsMedecinOrInfirmier])
def rechercher_dpi_par_nss(request, nss):
    try:
        dpi = DPI.objects.select_related('patient').get(nss=nss)
    except DPI.DoesNotExist:
        return Response({'detail': 'DPI non trouvé avec ce NSS.'}, status=status.HTTP_404_NOT_FOUND)
    
    patient_nom = dpi.patient.nom   
    return Response({'nom': patient_nom}, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method='patch',
    operation_description="Modifier un DPI existant avec l'ID spécifié. Accessible uniquement aux médecins.",
    request_body=DPISerializer,
    responses={
        200: DPISerializer,
        404: "DPI non trouvé.",
        400: "Erreur de validation des données."
    }
)
@api_view(['PATCH'])
@permission_classes([IsMedecin])
def modifier_dpi(request, dpi_id):
    """
    Modifier un DPI existant avec l'ID spécifié. 
    Cette vue est accessible uniquement aux médecins.
    """
    try:
        # Récupérer l'objet DPI en fonction de l'ID
        dpi = DPI.objects.get(nss=dpi_id)
    except DPI.DoesNotExist:
        return Response({'detail': 'DPI non trouvé.'}, status=status.HTTP_404_NOT_FOUND)
    
    # Sérialiser et mettre à jour les données du DPI
    serializer = DPISerializer(dpi, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='delete',
    operation_description="Supprimer un DPI existant avec l'ID spécifié. Accessible uniquement aux médecins.",
    manual_parameters=[
        openapi.Parameter('dpi_id', openapi.IN_PATH, description="ID du DPI à supprimer", type=openapi.TYPE_STRING, required=True)
    ],
    responses={
        204: "DPI supprimé avec succès.",
        404: "DPI non trouvé."
    }
)
@api_view(['DELETE'])
@permission_classes([IsMedecin])
def supprimer_dpi(request, dpi_id):
    """
    Supprimer un DPI existant avec l'ID spécifié. 
    Cette vue est accessible uniquement aux médecins.
    """
    try:
        # Récupérer l'objet DPI en fonction de l'ID
        dpi = DPI.objects.get(nss=dpi_id)
    except DPI.DoesNotExist:
        return Response({'detail': 'DPI non trouvé.'}, status=status.HTTP_404_NOT_FOUND)
    
    # Supprimer le DPI
    dpi.delete()
    return Response({'detail': 'DPI supprimé avec succès.'}, status=status.HTTP_204_NO_CONTENT)


@swagger_auto_schema(
    method='get',
    operation_description="Récupérer les informations détaillées du DPI d'un patient connecté via le token. Accessible uniquement aux patients.",
    responses={
        200: DPIDetailSerializer,
        404: "DPI non trouvé pour cet utilisateur."
    }
)
@api_view(['GET'])
@permission_classes([IsPatient])
def consulter_dpi_patient(request):
    # get the patient dpi with the token 
    try:
        dpi = DPI.objects.all().select_related('patient').get(patient_id=request.user.id)
    except DPI.DoesNotExist:
        return Response({'detail': 'DPI non trouvé pour cet utilisateur.'}, status=status.HTTP_404_NOT_FOUND)
    # Sérialisation et renvoi des données détaillées du DPI
    serializer = DPIDetailSerializer(dpi)
    nom = dpi.patient.nom
    response_data = serializer.data
    response_data['nom'] = nom
    return Response(response_data, status=status.HTTP_200_OK)
