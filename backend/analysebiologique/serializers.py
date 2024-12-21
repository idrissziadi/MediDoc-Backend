from rest_framework import serializers
from .models import AnalyseBiologique

class AnalyseBiologiqueSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour le modèle AnalyseBiologique.
    """
    
    class Meta:
        model = AnalyseBiologique
        fields = ['id_analyse_biologique', 'parametre_analyse', 'valeur', 'unite', 'bilan', 'laborantin']

class AnalyseBiologiqueDetailSerializer(serializers.ModelSerializer):
    laborantin = serializers.StringRelatedField()  # Affiche le nom du laborantin (ou tout autre champ __str__)

    class Meta:
        model = AnalyseBiologique
        fields = ['id_analyse_biologique', 'parametre_analyse', 'valeur', 'unite', 'bilan', 'laborantin']
