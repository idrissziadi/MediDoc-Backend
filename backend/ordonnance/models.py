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
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='non_valide')

    # Relation avec Consultation (une consultation peut avoir plusieurs ordonnances)
    consultation = models.ForeignKey(
        Consultation,
        on_delete=models.CASCADE,
        related_name='ordonnances'
    )

    def __str__(self):
        return f"Ordonnance {self.id_ordonnance} - {self.status} (Consultation ID: {self.consultation.id_consultation})"
