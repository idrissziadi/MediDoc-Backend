from rest_framework import serializers
from .models import Bilan

class BilanSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour le modèle Bilan.
    """
    
    class Meta:
        model = Bilan
        fields = ['id_bilan', 'type_bilan', 'description', 'consultation']
