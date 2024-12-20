from django.db import models
from django.contrib.auth import get_user_model
from DPI.models import DPI 

class Consultation(models.Model):
    """
    Modèle pour les consultations associées à un DPI.
    """
    id_consultation = models.AutoField(primary_key=True)
    date = models.DateField()
    resume = models.TextField()

    # Relations
    dpi = models.ForeignKey(DPI, on_delete=models.CASCADE, related_name='consultations') 
    medecin = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'medecin'},
        related_name='consultations'
    )

    def __str__(self):
        return f"Consultation {self.id_consultation} pour DPI {self.dpi.id} par médecin {self.medecin.username}"
