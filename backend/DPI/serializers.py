from rest_framework import serializers
from .models import DPI
from soins.serializers import SoinDetailSerializer
from consultations.serializers import ConsultationDetailSerializer
class DPISerializer(serializers.ModelSerializer):
    class Meta:
        model = DPI
        fields = ['nss', 'date_naissance', 'telephone', 'adresse', 'mutuelle', 'personne_contact', 'sexe', 'patient','medecin_traitant']

class DPIDetailSerializer(serializers.ModelSerializer):
    soins = SoinDetailSerializer(many=True)
    consultations = ConsultationDetailSerializer(many=True)

    class Meta:
        model = DPI
        fields = ['nss', 'date_naissance', 'telephone', 'adresse', 'mutuelle', 'personne_contact', 'sexe', 'soins', 'consultations']
