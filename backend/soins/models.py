from django.db import models
from django.conf import settings  # Pour utiliser AUTH_USER_MODEL
from DPI.models import DPI  # Assurez-vous d'importer le modèle DPI

class Soin(models.Model):
    """
    Modèle pour les soins réalisés sur un DPI.
    """
    id_soin = models.AutoField(primary_key=True)
    date = models.DateField()
    soins = models.CharField(max_length=255)
    observations = models.TextField(null=True, blank=True)  # Observations facultatives
    dpi = models.ForeignKey(DPI, on_delete=models.CASCADE, related_name='soins')  # Relation avec DPI (OneToMany)
    infirmier = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='soins_realises',limit_choices_to={'role': 'infirmier'})  # Relation avec l'utilisateur infirmier

    def __str__(self):
        return f"Soin {self.id_soin} pour DPI {self.dpi.id} par infirmier {self.infirmier.username}"
