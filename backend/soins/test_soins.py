import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from datetime import datetime

from DPI.models import DPI
from .models import Soin

User = get_user_model()


@pytest.fixture
def api_client():
    """Provides an instance of the DRF APIClient for each test."""
    return APIClient()


@pytest.fixture
def infirmier_user(db):
    """Create and return a user with the 'infirmier' role."""
    return User.objects.create_user(
        email='infirmier@example.com',
        nom='InfirmierUser',
        password='password123',
        role='infirmier',
        specialite='Infirmier'
    )


@pytest.fixture
def patient_user(db):
    """Create and return a user with the 'patient' role."""
    return User.objects.create_user(
        email='patient@example.com',
        nom='PatientUser',
        password='password123',
        role='patient',
        specialite='some_specialite'
    )


@pytest.fixture
def dpi(db, patient_user):
    """
    Create and return a DPI instance.
    IMPORTANT: We pass in a non-null `patient` to avoid IntegrityError.
    """
    return DPI.objects.create(
        nss='123456789',
        date_naissance='2000-01-01',
        telephone='1234567890',
        adresse='123 Main St',
        mutuelle='Mutuelle',
        personne_contact='Contact Person',
        sexe='M',
        patient=patient_user,  # Link the patient_user here
    )


@pytest.mark.django_db
class TestGetSoinsParDPI:
    """Test suite for the get_soins_par_dpi view."""

    def test_get_soins_par_dpi_success(self, api_client, infirmier_user, dpi):
        """
        Vérifie qu’un utilisateur infirmier peut récupérer la liste
        des soins pour un DPI existant.
        """
        # Create a test Soin
        Soin.objects.create(
            date=datetime.now(),
            soins='Test soin',
            observations='Test observation',
            dpi=dpi,
            infirmier=infirmier_user
        )

        api_client.force_authenticate(user=infirmier_user)
        url = reverse('get_soins_par_dpi', args=[dpi.nss])
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1  # We created exactly 1 Soin

    def test_get_soins_par_dpi_not_found(self, api_client, infirmier_user):
        """
        Vérifie qu’une erreur 404 est renvoyée si le DPI n’existe pas.
        """
        api_client.force_authenticate(user=infirmier_user)
        url = reverse('get_soins_par_dpi', args=['999999999'])
        response = api_client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data['detail'] == 'DPI spécifié introuvable.'


@pytest.mark.django_db
class TestAjouterSoins:
    """Test suite for the ajouterSoins view."""

    def test_ajouter_soins_success(self, api_client, infirmier_user, dpi):
        """
        Vérifie qu’un soin peut être ajouté avec succès par un infirmier.
        """
        api_client.force_authenticate(user=infirmier_user)
        url = reverse('ajouter-soins')
        data = {
            'soins': 'New soin',
            'observations': 'New observation',
            'dpi': dpi.nss
        }
        response = api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert Soin.objects.count() == 1

    def test_ajouter_soins_dpi_not_found(self, api_client, infirmier_user):
        """
        Vérifie qu’on ne peut pas ajouter un soin si le DPI n’existe pas.
        """
        api_client.force_authenticate(user=infirmier_user)
        url = reverse('ajouter-soins')
        data = {
            'soins': 'New soin',
            'observations': 'New observation',
            'dpi': '999999999'  # Non-existent DPI NSS
        }
        response = api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['detail'] == 'DPI spécifié introuvable.'


@pytest.mark.django_db
class TestSupprimerSoin:
    """Test suite for the supprimerSoin view."""

    def test_supprimer_soin_success(self, api_client, infirmier_user, dpi):
        """
        Vérifie qu’un soin peut être supprimé par un infirmier.
        """
        soin = Soin.objects.create(
            date=datetime.now(),
            soins='Test soin',
            observations='Test observation',
            dpi=dpi,
            infirmier=infirmier_user
        )

        api_client.force_authenticate(user=infirmier_user)
        url = reverse('supprimer_soin', args=[soin.id_soin])
        response = api_client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Soin.objects.count() == 0

    def test_supprimer_soin_not_found(self, api_client, infirmier_user):
        """
        Vérifie qu’une erreur 404 est renvoyée si le soin n’existe pas.
        """
        api_client.force_authenticate(user=infirmier_user)
        url = reverse('supprimer_soin', args=[999999])  # Non-existent Soin
        response = api_client.delete(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data['detail'] == 'Soin introuvable.'
