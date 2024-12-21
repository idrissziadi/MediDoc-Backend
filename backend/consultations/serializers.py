from rest_framework import serializers
from .models import Consultation
from bilans.serializers import BilanDetailSerializer
from ordonnance.serializers import OrdonnanceDetailSerializer
class ConsultationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consultation
        fields = '__all__'  # Inclut tous les champs du modèle

class ConsultationDetailSerializer(serializers.ModelSerializer):
    ordonnances = OrdonnanceDetailSerializer(many=True)
    bilans = BilanDetailSerializer(many=True)
    medecin = serializers.StringRelatedField()  # Affiche le nom du médecin (ou tout autre champ)

    class Meta:
        model = Consultation
        fields = ['id_consultation', 'date', 'resume', 'dpi', 'ordonnances', 'bilans', 'medecin']
