from rest_framework import serializers
from .models import Soin

class SoinSerializer(serializers.ModelSerializer):
    """
    Serializer pour le modèle Soin.
    """
    class Meta:
        model = Soin
        fields = ['id_soin', 'date', 'soins', 'observations', 'dpi', 'infirmier']
        extra_kwargs = {
            'observations': {'allow_null': True},  # Autoriser null pour observations
        }

class SoinDetailSerializer(serializers.ModelSerializer):
    infirmier = serializers.StringRelatedField()  # Affiche le nom de l'infirmier (ou tout autre champ)

    class Meta:
        model = Soin
        fields = ['id_soin', 'date', 'soins', 'observations', 'dpi', 'infirmier']
