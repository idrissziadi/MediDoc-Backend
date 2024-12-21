from rest_framework import serializers
from .models import Bilan
from analysebiologique.serializers import AnalyseBiologiqueDetailSerializer

class BilanSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour le modèle Bilan.
    """
    
    class Meta:
        model = Bilan
        fields = ['id_bilan', 'type_bilan', 'description', 'consultation']

class BilanDetailSerializer(serializers.ModelSerializer):
    analyses_biologiques = AnalyseBiologiqueDetailSerializer(many=True, source='analysebiologique_set')  # Inclut les analyses biologiques

    class Meta:
        model = Bilan
        fields = ['id_bilan', 'type_bilan', 'description', 'consultation', 'analyses_biologiques']
