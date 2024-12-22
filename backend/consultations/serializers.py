from rest_framework import serializers
from .models import Consultation
from ordonnance.serializers import OrdonnanceDetailSerializer
class ConsultationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consultation
        fields = '__all__'  # Inclut tous les champs du modèle
        extra_kwargs = {
            'resume': {'required': False}  # Ce champ n'est plus obligatoire
        }

class ConsultationDetailSerializer(serializers.ModelSerializer):
    ordonnances = OrdonnanceDetailSerializer(many=True)
     
    medecin = serializers.StringRelatedField()  # Affiche le nom du médecin (ou tout autre champ)

    class Meta:
        model = Consultation
        fields = ['id_consultation', 'date', 'resume', 'dpi', 'ordonnances', 'bilans', 'medecin']
