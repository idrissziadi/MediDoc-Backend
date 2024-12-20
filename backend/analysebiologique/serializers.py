from rest_framework import serializers
from .models import AnalyseBiologique

class AnalyseBiologiqueSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour le modèle AnalyseBiologique.
    """
    
    class Meta:
        model = AnalyseBiologique
        fields = ['id_analyse_biologique', 'parametre_analyse', 'valeur', 'unite', 'bilan', 'laborantin']
