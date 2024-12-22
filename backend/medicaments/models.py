from django.db import models

class Medicament(models.Model):
    """
    Modèle pour les médicaments.
    """
    id_medicament = models.AutoField(primary_key=True)  # Identifiant unique pour chaque médicament
    nom = models.CharField(max_length=255, unique=True)  # Nom du médicament
    code = models.CharField(max_length=100, unique=True)  # Code unique pour identification
    forme = models.CharField(max_length=100)  # Forme du médicament (ex: comprimé, sirop, gélule)

    def __str__(self):
        return f"{self.nom} ({self.forme})"
