from django.db import models
from ordonnance.models import Ordonnance

class Medicament(models.Model):
    """
    Modèle pour les médicaments.
    """
    id_medicament = models.AutoField(primary_key=True)  # Identifiant unique pour chaque médicament
    nom = models.CharField(max_length=255)  # Nom du médicament
    dose = models.CharField(max_length=10)  # Dose prescrite
    duree = models.CharField(max_length=15)  # Durée en jours
    ordonnance = models.ForeignKey(Ordonnance, on_delete=models.CASCADE, related_name='medicaments')  # Relation avec ordonnance (OneToMany)
     

    def __str__(self):
        return f"{self.nom})"
