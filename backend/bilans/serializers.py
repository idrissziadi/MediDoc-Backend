from rest_framework import serializers
from .models import AnalyseBiologique, ImageRadiologique

class ImageRadiologiqueSerializer(serializers.ModelSerializer):
    nss = serializers.CharField(source='consultation.dpi_id', read_only=True)
    date = serializers.DateField(source='consultation.date', read_only=True)
    
    class Meta:
        model = ImageRadiologique
        radiologue = serializers.StringRelatedField()
        fields = ['id_image_radiologique', 'type', 'url', 'compte_rendu', 'statut', 'nss', 'date']


class AnalyseBiologiqueSerializer(serializers.ModelSerializer):
    parametres = serializers.SerializerMethodField()
    nss = serializers.CharField(source='consultation.dpi_id', read_only=True)
    date = serializers.DateField(source='consultation.date', read_only=True)

    class Meta:
        model = AnalyseBiologique
        fields = ['id_analyse_biologique', 'type', 'parametres', 'statut', 'nss', 'date']

    def get_parametres(self, obj):
        """
        Convertit les champs parametre_analyse et valeur en une liste de dictionnaires.
        """
        parametres = obj.parametre_analyse.split('#') if obj.parametre_analyse else []
        valeurs = obj.valeur.split('#') if obj.valeur else []
        
        # Associer chaque paramètre avec sa valeur
        parametres_valeurs = [
            {"parametre": param, "valeur": float(val) if val else None}
            for param, val in zip(parametres, valeurs)
        ]
        return parametres_valeurs


# Custom Serializer for ImageRadiologique
class CustomImageRadiologiqueSerializer(serializers.ModelSerializer):
    nss = serializers.CharField(source='consultation.dpi_id', read_only=True)
    date = serializers.DateField(source='consultation.date', read_only=True)
    class Meta:
        model = ImageRadiologique
        fields = ['id_image_radiologique', 'type', 'url', 'compte_rendu', 'radiologue_id', 'statut', 'nss', 'date']
    

class ImageRadiologiqueUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageRadiologique
        fields = ['url', 'compte_rendu', 'radiologue', 'statut'] 


class AnalyseBiologiqueUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnalyseBiologique
        fields = ['parametre_analyse', 'valeur', 'laborantin', 'statut']