from rest_framework import serializers
from .models import DPI

class DPISerializer(serializers.ModelSerializer):
    class Meta:
        model = DPI
        fields = ['nss', 'nom', 'date_naissance', 'telephone', 'adresse', 'mutuelle', 'personne_contact', 'sexe', 'patient']
