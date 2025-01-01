from django.db import models
from ordonnance.models import Ordonnance  # Import du modèle Ordonnance
from medicaments.models import Medicament  # Import du modèle Medicament


class OrdonnanceHasMedicament(models.Model):
    """
    Modèle intermédiaire pour la relation Many-to-Many entre Ordonnance et Medicament.
    """
    ordonnance = models.ForeignKey(
        Ordonnance,
        on_delete=models.CASCADE,
        related_name='ordonnance_has_medicaments'
    )
    medicament = models.ForeignKey(
        Medicament,
        on_delete=models.CASCADE,
        related_name='ordonnance_has_medicaments'
    )

    # Champs supplémentaires
    dose = models.CharField(max_length=10)  # Dose prescrite
    duree = models.CharField(max_length=15)  # Durée en jours
    frequence = models.CharField(max_length=15)  # Fréquence d'administration par jour

    def __str__(self):
        return (f"Ordonnance {self.ordonnance.id_ordonnance} - Medicament {self.medicament.nom} | "
                f"Dose: {self.dose}, Durée: {self.duree} jours, Fréquence: {self.frequence} fois/jour")
