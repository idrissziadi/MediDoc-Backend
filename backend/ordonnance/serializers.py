from rest_framework import serializers
from .models import Ordonnance
from ordonnace_has_medicament.serializers import OrdonnanceHasMedicamentDetailSerializer

class OrdonnanceDetailSerializer(serializers.ModelSerializer):
    medicaments = OrdonnanceHasMedicamentDetailSerializer(many=True, source='ordonnance_has_medicaments')  # Inclut les médicaments

    class Meta:
        model = Ordonnance
        fields = ['id_ordonnance', 'status', 'medicaments']