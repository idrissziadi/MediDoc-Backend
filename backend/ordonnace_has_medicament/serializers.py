from rest_framework import serializers
from ordonnance.models import Ordonnance
from medicaments.models import Medicament
from .models import OrdonnanceHasMedicament
from medicaments.serializers import MedicamentSerializer

'''
class OrdonnanceHasMedicamentSerializer(serializers.ModelSerializer):
    """
    Serializer pour le modèle OrdonnanceHasMedicament.
    """
    ordonnance = serializers.PrimaryKeyRelatedField(queryset=Ordonnance.objects.all())
    medicament = serializers.PrimaryKeyRelatedField(queryset=Medicament.objects.all())

    class Meta:
        model = OrdonnanceHasMedicament
        fields = ['id', 'ordonnance', 'medicament', 'dose', 'duree', 'frequence']

class OrdonnanceHasMedicamentDetailSerializer(serializers.ModelSerializer):
    medicament = MedicamentSerializer()  # Inclut les détails du médicament

    class Meta:
        model = OrdonnanceHasMedicament
        fields = ['id', 'medicament', 'dose', 'duree', 'frequence']

   '''

class MedicamentDetailSerializer(serializers.ModelSerializer):
    nom = serializers.CharField(source='medicament.nom', read_only=True)
    class Meta:
        model = OrdonnanceHasMedicament
        fields = ['nom', 'dose', 'duree', 'frequence']
        depth = 1      


