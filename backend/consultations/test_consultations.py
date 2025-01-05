import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model
from datetime import datetime

from consultations.models import Consultation
from DPI.models import DPI
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Consultation
from bilans.models import AnalyseBiologique, ImageRadiologique
from ordonnance.models import Ordonnance
from medicaments.models import Medicament
from .serializers import ConsultationSerializer, ConsultationDetailSerializer
from .permissions import IsMedecin, IsPatientOrMedecin

User = get_user_model()

@pytest.fixture
def api_client():
    """
    Provides a DRF APIClient instance for each test.
    """
    return APIClient()

@pytest.fixture
def medecin_user(db):
    """
    Create and return a user with the 'medecin' role.
    """
    return User.objects.create_user(
        email='medecin@example.com',
        nom='TestMedecin',
        password='password123',
        role='medecin',
        specialite='Cardiologie',  # or any valid value required by your custom user model
    )

@pytest.fixture
def patient_user(db):
    """
    Create and return a user with the 'patient' role (for testing permission).
    """
    return User.objects.create_user(
        email='patient@example.com',
        nom='TestPatient',
        password='password123',
        role='patient',
        specialite='other',  # or any valid value
    )

@pytest.fixture
def dpi_instance(db, patient_user):
    """
    Create and return a DPI instance for testing.
    """
    return DPI.objects.create(
        nss='123456789',
        date_naissance='1990-01-01',
        telephone='0606060606',
        adresse='Patient Address',
        mutuelle='TestMutuelle',
        personne_contact='Emergency Contact',
        sexe='M',
        patient=patient_user
    )

@pytest.fixture
def consultation_instance(db, dpi_instance, medecin_user):
    """
    Create and return a Consultation instance for testing.
    """
    return Consultation.objects.create(
        date='2024-01-01',
        resume='Existing consultation data',
        dpi=dpi_instance,
        medecin=medecin_user
    )

@pytest.mark.django_db
class TestGetAllConsultations:
    def test_get_all_consultations_as_medecin(self, api_client, medecin_user, consultation_instance):
        """
        A user with role='medecin' can retrieve all consultations.
        """
        # Force authentication with medecin role
        api_client.force_authenticate(user=medecin_user)

        url = reverse("get_all_consultations")  # from urls.py => path('', views.get_all_consultations, ...)
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) >= 1

    def test_get_all_consultations_as_patient_forbidden(self, api_client, patient_user):
        """
        A user with role='patient' should be forbidden from retrieving consultations.
        """
        api_client.force_authenticate(user=patient_user)

        url = reverse("get_all_consultations")
        response = api_client.get(url)

        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
class TestGetConsultationById:
    def test_get_consultation_by_id_ok(self, api_client, medecin_user, consultation_instance):
        """
        A medecin user can retrieve a specific consultation by ID.
        """
        api_client.force_authenticate(user=medecin_user)
        url = reverse("get_consultation_by_id", kwargs={"id_consultation": consultation_instance.id_consultation})
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id_consultation"] == consultation_instance.id_consultation

    def test_get_consultation_by_id_not_found(self, api_client, medecin_user):
        """
        Requesting a consultation that doesn't exist should return 404.
        """
        api_client.force_authenticate(user=medecin_user)
        url = reverse("get_consultation_by_id", kwargs={"id_consultation": 999999})
        response = api_client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "Consultation non trouvée" in response.data["detail"]

    def test_get_consultation_by_id_as_patient_forbidden(self, api_client, patient_user, consultation_instance):
        """
        A patient user shouldn't be able to retrieve a consultation.
        """
        api_client.force_authenticate(user=patient_user)
        url = reverse("get_consultation_by_id", kwargs={"id_consultation": consultation_instance.id_consultation})
        response = api_client.get(url)

        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
class TestCreateConsultation:
    def test_create_consultation_success(self, api_client, medecin_user, dpi_instance):
        """
        A medecin user can create a new consultation.
        """
        api_client.force_authenticate(user=medecin_user)
        url = reverse("create_consultation")  # path('creer/', views.create_consultation, name='create_consultation')

        data = {
            "date": "2024-05-05",
            "resume": "Some consultation notes",
            "dpi": dpi_instance.nss,  # ForeignKey to DPI
        }
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert Consultation.objects.filter(dpi=dpi_instance, resume="Some consultation notes").exists()

    def test_create_consultation_as_patient_forbidden(self, api_client, patient_user, dpi_instance):
        api_client.force_authenticate(user=patient_user)
        url = reverse("create_consultation")
        data = {
            "date": "2024-05-05",
            "resume": "Invalid attempt",
            "dpi": dpi_instance.nss,
        }
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
class TestUpdateConsultation:
    def test_update_consultation_success(self, api_client, medecin_user, consultation_instance):
        """
        A medecin user can update an existing consultation.
        """
        api_client.force_authenticate(user=medecin_user)
        url = reverse("update_consultation", kwargs={"id_consultation": consultation_instance.id_consultation})

        data = {
            "resume": "Updated consultation notes"
        }
        response = api_client.put(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        consultation_instance.refresh_from_db()
        assert consultation_instance.resume == "Updated consultation notes"

    def test_update_consultation_not_found(self, api_client, medecin_user):
        """
        Trying to update a non-existent consultation should return 404.
        """
        api_client.force_authenticate(user=medecin_user)
        url = reverse("update_consultation", kwargs={"id_consultation": 999999})
        data = {"resume": "Should fail"}
        response = api_client.put(url, data, format='json')
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "Consultation non trouvée" in response.data["detail"]

    def test_update_consultation_as_patient_forbidden(self, api_client, patient_user, consultation_instance):
        api_client.force_authenticate(user=patient_user)
        url = reverse("update_consultation", kwargs={"id_consultation": consultation_instance.id_consultation})
        data = {"resume": "Attempting update"}
        response = api_client.put(url, data, format='json')
        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
class TestDeleteConsultation:
    def test_delete_consultation_success(self, api_client, medecin_user, consultation_instance):
        """
        A medecin user can delete an existing consultation.
        """
        api_client.force_authenticate(user=medecin_user)
        url = reverse("delete_consultation", kwargs={"id_consultation": consultation_instance.id_consultation})
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Consultation.objects.filter(id_consultation=consultation_instance.id_consultation).exists()

    def test_delete_consultation_not_found(self, api_client, medecin_user):
        """
        Deleting a non-existent consultation should return 404.
        """
        api_client.force_authenticate(user=medecin_user)
        url = reverse("delete_consultation", kwargs={"id_consultation": 999999})
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "Consultation non trouvée" in response.data["detail"]

    def test_delete_consultation_as_patient_forbidden(self, api_client, patient_user, consultation_instance):
        api_client.force_authenticate(user=patient_user)
        url = reverse("delete_consultation", kwargs={"id_consultation": consultation_instance.id_consultation})
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

@pytest.mark.django_db
class TestCreerConsultationAvecOrdonnace:
    def test_creer_consultation_avec_ordonnace_success(self, api_client, medecin_user, dpi_instance):
        """
        A medecin user can create a consultation and associated ordonnance + meds.
        """
        api_client.force_authenticate(user=medecin_user)
        url = reverse("creerConsultationAvecOrdonnace")

        data = {
            "resume": "Consultation with an ordonnance",
            "dpi": dpi_instance.nss,
            "ordonnance": {
                "medicaments": [
                    {
                        "nom": "TestMedicament",
                        "dose": "500mg",
                        "duree": "5 days"
                    }
                ]
            }
        }

        response = api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert Consultation.objects.filter(dpi=dpi_instance, resume="Consultation with an ordonnance").exists()
        assert Ordonnance.objects.filter(consultation__dpi=dpi_instance).exists()
        assert Medicament.objects.filter(
            nom="TestMedicament",
            dose="500mg",
            duree="5 days",
            ordonnance__consultation__dpi=dpi_instance
        ).exists()

@pytest.mark.django_db
class TestCreerConsultationAvecBilan:
    def test_creer_consultation_avec_bilan_success(
        self, api_client, medecin_user, dpi_instance
    ):
        """
        A medecin user can create a consultation and request bilans (analyses / images).
        """
        api_client.force_authenticate(user=medecin_user)
        url = reverse("creerConsultationAvecBilan")

        data = {
            "date": "2024-07-01",
            "resume": "Consultation requesting bilans",
            "dpi": dpi_instance.nss,
            "analyses_biologiques": [
                {"type": "Blood Test"},
                {"type": "Urine Test"},
            ],
            "images_radiologiques": [
                {"type": "X-Ray"},
                {"type": "MRI"},
            ],
        }

        response = api_client.post(url, data, format='json')
        # Depending on your setup, you might need to have the related models, foreign keys, etc. in place
        # to ensure no 404 or other errors occur.
        @api_view(['GET'])
        @permission_classes([IsMedecin])
        def get_all_consultations(request):
            consultations = Consultation.objects.all()
            serializer = ConsultationSerializer(consultations, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        @api_view(['GET'])
        @permission_classes([IsMedecin])
        def get_consultation_by_id(request, id_consultation):
            try:
                consultation = Consultation.objects.get(id_consultation=id_consultation)
            except Consultation.DoesNotExist:
                return Response({'detail': 'Consultation non trouvée.'}, status=status.HTTP_404_NOT_FOUND)

            serializer = ConsultationSerializer(consultation)
            return Response(serializer.data, status=status.HTTP_200_OK)

        @api_view(['POST'])
        @permission_classes([IsMedecin])
        def create_consultation(request):
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
            try:
                consultation = Consultation.objects.get(id_consultation=id_consultation)
            except Consultation.DoesNotExist:
                return Response({'detail': 'Consultation non trouvée.'}, status=status.HTTP_404_NOT_FOUND)

            consultation.delete()
            return Response({'detail': 'Consultation supprimée avec succès.'}, status=status.HTTP_204_NO_CONTENT)

        @api_view(['POST'])
        @permission_classes([IsMedecin])
        def creerConsultationAvecOrdonnance(request):
            medecin_id = request.user.id
            data = request.data.copy()

            try:
                consultation_data = {
                    "date": datetime.datetime.now().strftime('%Y-%m-%d'),
                    "resume": data.get("resume"),
                    "dpi": data.get("dpi"),
                    "medecin": medecin_id
                }
                consultation_serializer = ConsultationSerializer(data=consultation_data)
                if not consultation_serializer.is_valid():
                    return Response(consultation_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                consultation = consultation_serializer.save()

                ordonnance_data = data.get("ordonnance", {})
                ordonnance = Ordonnance.objects.create(
                    consultation=consultation,
                    status=ordonnance_data.get("status", "non_valide")
                )

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
            medecin_id = request.user.id
            data = request.data.copy()

            try:
                consultation_data = {
                    "date": datetime.datetime.now().strftime('%Y-%m-%d'),
                    "resume": data.get("resume"),
                    "dpi": data.get("dpi"),
                    "medecin": medecin_id
                }
                consultation_serializer = ConsultationSerializer(data=consultation_data)
                if not consultation_serializer.is_valid():
                    return Response(consultation_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                consultation = consultation_serializer.save()

                analyses_data = data.get("analyses_biologiques", [])
                for analyse_data in analyses_data:
                    AnalyseBiologique.objects.create(
                        type=analyse_data.get("type"),
                        consultation=consultation
                    )

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
            try:
                consultations = Consultation.objects.filter(dpi_id=id_dpi)
                if not consultations.exists():
                    return Response({'detail': 'Aucune consultation trouvée pour ce patient.'}, status=status.HTTP_404_NOT_FOUND)

                serializer = ConsultationDetailSerializer(consultations, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)

            except Exception as e:
                return Response({"detail": f"Une erreur s'est produite: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
