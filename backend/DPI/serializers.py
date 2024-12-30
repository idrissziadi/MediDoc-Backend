from rest_framework import serializers
from .models import DPI
class DPISerializer(serializers.ModelSerializer):
    class Meta:
        model = DPI
        fields = ['nss', 'date_naissance', 'telephone', 'adresse', 'mutuelle', 'personne_contact', 'sexe', 'patient','medecin_traitant']


class DPIDetailSerializer(serializers.ModelSerializer):
    patient = serializers.CharField(source='patient.nom', read_only=True)   
    medecin_traitant = serializers.CharField(source='medecin_traitant.nom', read_only=True)
    class Meta:
        model = DPI
        fields = ['nss', 'date_naissance', 'telephone', 'adresse', 'mutuelle', 'personne_contact', 'sexe', 'patient','medecin_traitant']