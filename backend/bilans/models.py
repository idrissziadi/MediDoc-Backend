from django.db import models
from django.contrib.auth import get_user_model
from DPI.models import DPI
from consultations.models import Consultation       

class Bilan(models.Model):
    """
    Modèle pour les bilans associés à une consultation.
    """
    # Définir l'énumération des types de bilan
    RADIOLOGIQUE = 'radiologique'
    BIOLOGIQUE = 'biologique'
    
    TYPE_BILAN_CHOICES = [
        (RADIOLOGIQUE, 'Radiologique'),
        (BIOLOGIQUE, 'Biologique')
    ]
    
    # Champs de base
    id_bilan = models.AutoField(primary_key=True)
    type_bilan = models.CharField(max_length=20, choices=TYPE_BILAN_CHOICES)
    description = models.CharField(max_length=255, null=True, blank=True)

    # Relation avec la consultation
    consultation = models.ForeignKey(Consultation, on_delete=models.CASCADE, related_name='bilans')

    def __str__(self):
        return f"Bilan {self.id_bilan} ({self.get_type_bilan_display()}) pour consultation {self.consultation.id_consultation}"
