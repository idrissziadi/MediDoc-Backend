from rest_framework import serializers
from .models import Ordonnance
from medicaments.serializers import MedicamentSerializer

'''
class OrdonnanceDetailSerializer(serializers.ModelSerializer):
    medicaments = OrdonnanceHasMedicamentDetailSerializer(many=True, source='ordonnance_has_medicaments')  # Inclut les médicaments

    class Meta:
        model = Ordonnance
        fields = ['id_ordonnance', 'status', 'medicaments']

        '''

class OrdonnanceDetailSerializer(serializers.ModelSerializer):
    nom_medecin = serializers.CharField(source='consultation.medecin.nom', read_only=True)
    medicaments = MedicamentSerializer(many=True, read_only=True)
    date = serializers.DateField(source='consultation.date', read_only=True)

    class Meta:
        model = Ordonnance
        fields = ['id_ordonnance', 'date', 'nom_medecin', 'medicaments']