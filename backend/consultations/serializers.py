from rest_framework import serializers
from .models import Consultation
from ordonnance.serializers import OrdonnanceDetailSerializer
from bilans.serializers import AnalyseBiologiqueDetailSerializer, ImageRadiologiqueDetailSerializer
class ConsultationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consultation
        fields = '__all__'  # Inclut tous les champs du modèle
        extra_kwargs = {
            'resume': {'required': False}  # Ce champ n'est plus obligatoire
        }

class ConsultationDetailSerializer(serializers.ModelSerializer):
    ordonnances = OrdonnanceDetailSerializer(many=True)
    analyses_biologiques = AnalyseBiologiqueDetailSerializer(many=True)
    images_radiologiques = ImageRadiologiqueDetailSerializer(many=True)
     
    medecin = serializers.StringRelatedField()  # Affiche le nom du médecin (ou tout autre champ)

    class Meta:
        model = Consultation
        fields = ['id_consultation', 'date', 'resume', 'ordonnances','analyses_biologiques', 'images_radiologiques', 'medecin']
