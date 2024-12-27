from django.db import models
from django.contrib.auth import get_user_model
from consultations.models import Consultation

# Create your models here.

class AnalyseBiologique(models.Model):
    STATUS_CHOICES = [
        ('terminé', 'Terminé'),
        ('pas_terminé', 'Pas_terminé'),
    ]

    id_analyse_biologique = models.AutoField(primary_key=True)
    type = models.CharField(max_length=45)
    parametre_analyse = models.CharField(max_length=100,null=True)
    valeur = models.CharField(max_length=100,null=True)
    unite = models.CharField(max_length=10,null=True)
    laborantin = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, limit_choices_to={'role': 'laborantin'},null=True,related_name='analyses_biologiques')
    statut = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pas_terminé')

    consultation = models.ForeignKey(
        Consultation, 
        on_delete=models.CASCADE, 
        related_name='analyses_biologiques'
    )

    def __str__(self):
        return f"Analyse {self.type} - {self.parametre_analyse}"
    


class ImageRadiologique(models.Model):
    STATUS_CHOICES = [
        ('terminé', 'Terminé'),
        ('pas_terminé', 'Pas_terminé'),
    ]
    id_image_radiologique = models.AutoField(primary_key=True)
    type = models.CharField(max_length=45,null=True)
    url = models.URLField(max_length=1000,null=True)
    compte_rendu = models.TextField(null=True)
    radiologue = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, limit_choices_to={'role': 'radiologue'},null=True,related_name='images_radiologiques')
    statut = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pas_terminé')

    consultation = models.ForeignKey(
        Consultation, 
        on_delete=models.CASCADE, 
        related_name='images_radiologiques'
    )

    def __str__(self):
        return f"Image {self.type} - {self.date}"
 