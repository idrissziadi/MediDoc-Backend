from rest_framework import serializers
from .models import Medicament


class MedicamentSerializer(serializers.ModelSerializer):
    """
    Serializer pour le modèle Medicament.
    """
    class Meta:
        model = Medicament
        fields = [ 'nom', 'dose', 'duree']
