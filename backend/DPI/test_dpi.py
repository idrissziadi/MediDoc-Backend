import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model

from .models import DPI

User = get_user_model()


@pytest.fixture
def api_client():
    """
    Provides an instance of the DRF APIClient for each test.
    """
    return APIClient()


@pytest.fixture
def administratif_user(db):
    """
    Create and return a user with the 'administratif' role.
    """
    return User.objects.create_user(
        email='admin@example.com',
        nom='AdminUser',
        password='password123',
        role='administratif',
        specialite='some_specialite'
    )


@pytest.fixture
def medecin_user(db):
    """
    Create and return a user with the 'medecin' role.
    """
    return User.objects.create_user(
        email='medecin@example.com',
        nom='MedecinUser',
        password='password123',
        role='medecin',
        specialite='some_specialite'
    )


@pytest.fixture
def patient_user(db):
    """
    Create and return a user with the 'patient' role.
    """
    return User.objects.create_user(
        email='patient@example.com',
        nom='PatientUser',
        password='password123',
        role='patient',
        specialite='some_specialite'
    )


@pytest.mark.django_db
class TestCreerDPI:
    """
    Test suite for the creer_dpi view.
    """

    def test_creer_dpi_success(self, api_client, administratif_user):
        """
        Test that an administratif user can successfully create a DPI.
        """
        # Force authentication
        api_client.force_authenticate(user=administratif_user)

        # Prepare data required by the creer_dpi view
        data = {
            "nss": "123456789",
            "date_naissance": "1990-01-01",
            "telephone": "0606060606",
            "adresse": "123 Rue Example",
            "mutuelle": "MutuelleX",
            "personne_contact": "John Doe",
            "sexe": "M",
            
            # Data for the user creation part
            "patient_nom": "NewPatient",
            "patient_email": "new_patient@example.com",
            "patient_password": "pass123",
        }

        url = reverse("creer_dpi")  # Adjust if your URL name is different
        response = api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_201_CREATED, response.data
        assert DPI.objects.filter(nss="123456789").exists()

    def test_creer_dpi_duplicate_nss(self, api_client, administratif_user):
        """
        Test that creating a DPI with an existing NSS returns a 400 error.
        """
        api_client.force_authenticate(user=administratif_user)

        # Create an existing DPI
        DPI.objects.create(
            nss="999999999",
            date_naissance="1980-01-01",
            telephone="0101010101",
            adresse="Old Address",
            mutuelle="OldMutuelle",
            personne_contact="Someone",
            sexe="F",
            patient=User.objects.create_user(
                email='existingpatient@example.com',
                nom='ExistingPatient',
                password='password123',
                role='patient',
                specialite='some_specialite'
            ),
        )

        data = {
            "nss": "999999999",  # same as above
            "date_naissance": "1990-01-01",
            "telephone": "0606060606",
            "adresse": "123 Rue Example",
            "mutuelle": "MutuelleX",
            "sexe": "M",
            "patient_nom": "NewPatient2",
            "patient_email": "new_patient2@example.com",
            "patient_password": "pass1234",
        }

        url = reverse("creer_dpi")
        response = api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "existe déjà" in str(response.data["detail"])


@pytest.mark.django_db
class TestConsulterDPI:
    """
    Test suite for the consulter_dpi view.
    """

    def test_consulter_dpi_as_patient(self, api_client, patient_user):
        @pytest.mark.django_db
        class TestConsulterDPI:
            """
            Test suite for the consulter_dpi view.
            """

            def test_consulter_dpi_as_patient(self, api_client, patient_user):
                """
                Test that a patient (the owner of the DPI) or medecin can consult a DPI.
                """
                # Create DPI with the patient_user
                dpi = DPI.objects.create(
                    nss="111111111",
                    date_naissance="1995-04-12",
                    telephone="0712345678",
                    adresse="Patient Address",
                    mutuelle="MyMutuelle",
                    personne_contact="Jane Doe",
                    sexe="F",
                    patient=patient_user,
                )

                api_client.force_authenticate(user=patient_user)

                # Suppose your URL pattern is something like path('dpi/<int:nss>/', consulter_dpi, name='consulter_dpi')
                url = reverse("consulter_dpi", kwargs={"nss": dpi.nss})
                response = api_client.get(url, format='json')

                assert response.status_code == status.HTTP_200_OK
                assert response.data["patient"]["nom"] == patient_user.nom

            def test_consulter_dpi_as_medecin(self, api_client, medecin_user, patient_user):
                """
                Test that a medecin can consult a patient's DPI.
                """
                # Create DPI with the patient_user
                dpi = DPI.objects.create(
                    nss="111111112",
                    date_naissance="1995-04-12",
                    telephone="0712345678",
                    adresse="Patient Address",
                    mutuelle="MyMutuelle",
                    personne_contact="Jane Doe",
                    sexe="F",
                    patient=patient_user,
                )

                api_client.force_authenticate(user=medecin_user)

                url = reverse("consulter_dpi", kwargs={"nss": dpi.nss})
                response = api_client.get(url, format='json')

                assert response.status_code == status.HTTP_200_OK
                assert response.data["patient"]["nom"] == patient_user.nom

            def test_consulter_dpi_not_found(self, api_client, patient_user):
                """
                Test that consulting a non-existent DPI returns 404.
                """
                api_client.force_authenticate(user=patient_user)
                url = reverse("consulter_dpi", kwargs={"nss": "999999998"})  # Non-existent
                response = api_client.get(url, format='json')

                assert response.status_code == status.HTTP_404_NOT_FOUND
                assert "non trouvé" in str(response.data["detail"])

            def test_consulter_dpi_unauthorized(self, api_client, patient_user):
                """
                Test that an unauthorized user cannot consult a DPI.
                """
                # Create DPI with the patient_user
                dpi = DPI.objects.create(
                    nss="111111113",
                    date_naissance="1995-04-12",
                    telephone="0712345678",
                    adresse="Patient Address",
                    mutuelle="MyMutuelle",
                    personne_contact="Jane Doe",
                    sexe="F",
                    patient=patient_user,
                )

                # Do not authenticate the client
                url = reverse("consulter_dpi", kwargs={"nss": dpi.nss})
                response = api_client.get(url, format='json')

                assert response.status_code == status.HTTP_403_FORBIDDEN

@pytest.mark.django_db
class TestRechercherDpiParNss:
    """
    Test suite for the rechercher_dpi_par_nss view.
    """

    def test_rechercher_dpi_par_nss_success(self, api_client, medecin_user):
        """
        A medecin or infirmier can search a DPI by NSS.
        """
        # Create a DPI
        patient = User.objects.create_user(
            email='patient2@example.com',
            nom='Patient2',
            password='password123',
            role='patient',
            specialite='some_specialite'
        )
        dpi = DPI.objects.create(
            nss="222222222",
            date_naissance="1998-05-05",
            telephone="0788888888",
            adresse="Some Address",
            mutuelle="TestMutuelle",
            personne_contact="Contact Person",
            sexe="F",
            patient=patient,
        )

        api_client.force_authenticate(user=medecin_user)

        # Suppose your URL is path('dpi/rechercher/<int:nss>/', rechercher_dpi_par_nss, name='rechercher_dpi_par_nss')
        url = reverse("rechercher_dpi_par_nss", kwargs={"nss": dpi.nss})
        response = api_client.get(url, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert response.data["nom"] == "Patient2"

    def test_rechercher_dpi_par_nss_not_found(self, api_client, medecin_user):
        api_client.force_authenticate(user=medecin_user)
        url = reverse("rechercher_dpi_par_nss", kwargs={"nss": "999999998"})
        response = api_client.get(url, format='json')

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "DPI non trouvé" in str(response.data["detail"])


@pytest.mark.django_db
class TestModifierDPI:
    """
    Test suite for the modifier_dpi view.
    """

    def test_modifier_dpi_as_medecin(self, api_client, medecin_user):
        """
        Only a medecin should be able to PATCH a DPI.
        """
        patient = User.objects.create_user(
            email='patient3@example.com',
            nom='Patient3',
            password='password123',
            role='patient',
            specialite='some_specialite'
        )
        dpi = DPI.objects.create(
            nss="333333333",
            date_naissance="1970-10-10",
            telephone="0707070707",
            adresse="Old Address",
            mutuelle="Mutuelle333",
            personne_contact="Old Contact",
            sexe="M",
            patient=patient,
        )

        api_client.force_authenticate(user=medecin_user)
        url = reverse("modifier_dpi", kwargs={"dpi_id": dpi.nss})
        data = {
            "adresse": "New Address Updated",
            "telephone": "0700000000",
        }
        response = api_client.patch(url, data, format='json')

        assert response.status_code == status.HTTP_200_OK
        dpi.refresh_from_db()
        assert dpi.adresse == "New Address Updated"
        assert dpi.telephone == "0700000000"

    def test_modifier_dpi_not_found(self, api_client, medecin_user):
        api_client.force_authenticate(user=medecin_user)
        url = reverse("modifier_dpi", kwargs={"dpi_id": "999999999"})
        data = {
            "adresse": "Should not matter",
        }
        response = api_client.patch(url, data, format='json')
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "DPI non trouvé" in str(response.data["detail"])


@pytest.mark.django_db
class TestSupprimerDPI:
    """
    Test suite for the supprimer_dpi view.
    """

    def test_supprimer_dpi_as_medecin(self, api_client, medecin_user):
        """
        Only a medecin should be able to DELETE a DPI.
        """
        patient = User.objects.create_user(
            email='patient4@example.com',
            nom='Patient4',
            password='password123',
            role='patient',
            specialite='some_specialite'
        )
        dpi = DPI.objects.create(
            nss="444444444",
            date_naissance="1985-02-02",
            telephone="0766666666",
            adresse="Address 444",
            mutuelle="Mutuelle444",
            personne_contact="Contact 444",
            sexe="F",
            patient=patient,
        )

        api_client.force_authenticate(user=medecin_user)
        url = reverse("supprimer_dpi", kwargs={"dpi_id": dpi.nss})
        response = api_client.delete(url, format='json')

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not DPI.objects.filter(nss="444444444").exists()

    def test_supprimer_dpi_not_found(self, api_client, medecin_user):
        api_client.force_authenticate(user=medecin_user)
        url = reverse("supprimer_dpi", kwargs={"dpi_id": "999999999"})
        response = api_client.delete(url, format='json')

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "DPI non trouvé" in str(response.data["detail"])
