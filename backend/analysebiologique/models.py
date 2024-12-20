from django.db import models
from django.conf import settings  # Pour utiliser AUTH_USER_MODEL
from bilans.models import Bilan  # Assurez-vous d'importer le modèle Bilan

class AnalyseBiologique(models.Model):
    """
    Modèle pour les analyses biologiques associées à un bilan.
    """
    # Identifiant unique pour chaque analyse biologique
    id_analyse_biologique = models.AutoField(primary_key=True)

    # Paramètres d'analyse possibles (avec des choix d'énumération)
    PARAMETRE_ANALYSE_CHOICES = [
        ('Fer', 'Fer'),
        ('Hypertension', 'Hypertension'),
        ('Glycémie', 'Glycémie'),
    ]
    parametre_analyse = models.CharField(max_length=50, choices=PARAMETRE_ANALYSE_CHOICES)

    # Valeur de l'analyse (float)
    valeur = models.FloatField()

    # Unités de mesure possibles (avec des choix d'énumération)
    UNITE_CHOICES = [
        ('mg/m3', 'mg/m3'),
        ('µmol/litre', 'µmol/litre'),
        ('mmol/24h', 'mmol/24h'),
    ]
    unite = models.CharField(max_length=20, choices=UNITE_CHOICES)

    # Relations avec le modèle Bilan
    bilan = models.ForeignKey(Bilan, on_delete=models.CASCADE, related_name='analyses_biologiques')

    # Relation avec l'utilisateur de rôle 'laborantin'
    laborantin = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        limit_choices_to={'role': 'laborantin'}, 
        related_name='analyses_biologiques'
    )

    def __str__(self):
        return f"Analyse biologique {self.id_analyse_biologique} - {self.parametre_analyse} : {self.valeur} {self.unite}"
