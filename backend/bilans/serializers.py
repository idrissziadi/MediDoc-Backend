from rest_framework import serializers
from .models import AnalyseBiologique, ImageRadiologique

class AnalyseBiologiqueDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnalyseBiologique
        laborantin = serializers.StringRelatedField()
        fields = ['id_analyse_biologique', 'type', 'parametre_analyse', 'valeur', 'unite', 'laborantin']

class ImageRadiologiqueDetailSerializer(serializers.ModelSerializer):
     
    class Meta:
        model = ImageRadiologique
        radiologue = serializers.StringRelatedField()
        fields = ['id_image_radiologique', 'type', 'url', 'compte_rendu', 'radiologue']        

