from django.db import models
from DPI.models import DPI
from consultations.models import Consultation 

class Ordonnance(models.Model):
    """
    Modèle pour les ordonnances.
    """
    STATUS_CHOICES = [
        ('valide', 'Valide'),
        ('non_valide', 'Non valide'),
    ]

    id_ordonnance = models.AutoField(primary_key=True)

    # Relation avec Consultation (une consultation peut avoir plusieurs ordonnances)
    consultation = models.OneToOneField(
        Consultation,
        on_delete=models.CASCADE,
        related_name='ordonnance'
    )

    def __str__(self):
        return f"Ordonnance {self.id_ordonnance} (Consultation ID: {self.consultation.id_consultation})"
