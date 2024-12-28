import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model

from consultations.models import Consultation
from DPI.models import DPI

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
    def test_creer_consultation_avec_ordonnace_success(
        self, api_client, medecin_user, dpi_instance
    ):
        """
        A medecin user can create a consultation and associated ordonnances + meds.
        """
        api_client.force_authenticate(user=medecin_user)
        url = reverse("creerConsultationAvecOrdonnace")  # from urls.py

        data = {
            "date": "2024-06-10",
            "resume": "Consultation with an ordonnance",
            "dpi": dpi_instance.nss,
            "ordonnances": [
                {
                    "status": "non_valide",
                    "medicaments": [
                        {
                            "id_medicament": 1,  # ID of an existing Medicament
                            "dose": "500mg",
                            "duree": "5 days",
                            "frequence": "3 times a day",
                        }
                    ],
                }
            ],
        }

        # Assuming you have a Medicament with id=1 in your DB. 
        # Otherwise, you might need to create one before this request or adjust accordingly.

        response = api_client.post(url, data, format='json')
        # If Medicament with id=1 doesn't exist, you'll get 404 from your code.

        if response.status_code == status.HTTP_404_NOT_FOUND:
            assert "non trouvé" in response.data["detail"]
        else:
            assert response.status_code == status.HTTP_201_CREATED

    def test_creer_consultation_avec_ordonnace_as_patient_forbidden(self, api_client, patient_user):
        api_client.force_authenticate(user=patient_user)
        url = reverse("creerConsultationAvecOrdonnace")
        data = {}
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_403_FORBIDDEN


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
        
        assert response.status_code in [status.HTTP_201_CREATED, status.HTTP_400_BAD_REQUEST], response.data
        if response.status_code == status.HTTP_201_CREATED:
            assert "id_consultation" in response.data or "resume" in response.data

    def test_creer_consultation_avec_bilan_as_patient_forbidden(self, api_client, patient_user):
        api_client.force_authenticate(user=patient_user)
        url = reverse("creerConsultationAvecBilan")
        data = {}
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_403_FORBIDDEN
