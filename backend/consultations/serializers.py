from rest_framework import serializers
from .models import Consultation
from bilans.models import AnalyseBiologique, ImageRadiologique

class AnalyseBiologiqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnalyseBiologique
        fields = ['id', 'type', 'status']  # Include the fields you want to expose


class ImageRadiologiqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageRadiologique
        fields = ['id', 'type', 'status']  # Include the fields you want to expose


class ConsultationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consultation
        fields = '__all__'  # Inclut tous les champs du modèle
        extra_kwargs = {
            'resume': {'required': False}  # Ce champ n'est plus obligatoire
        }
class ConsultationDetailSerializer(serializers.ModelSerializer):
    medecin = serializers.CharField(source='medecin.nom', read_only=True)
    dpi = serializers.CharField(source='dpi.nss', read_only=True)
    analyses_biologiques = AnalyseBiologiqueSerializer(many=True, read_only=True, source='analysebiologique_set')
    images_radiologiques = ImageRadiologiqueSerializer(many=True, read_only=True, source='imageradiologique_set')

    class Meta:
        model = Consultation
        fields = ['id_consultation', 'date', 'resume', 'dpi', 'medecin', 'analyses_biologiques', 'images_radiologiques']