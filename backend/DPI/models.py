from django.db import models
from django.contrib.auth import get_user_model

class DPI(models.Model):
    SEXE_CHOICES = [
        ('M', 'Masculin'),
        ('F', 'Féminin'),
    ]

    # Champs du modèle DPI
    nss = models.BigIntegerField(primary_key=True)
    date_naissance = models.DateField()
    telephone = models.CharField(max_length=15)
    adresse = models.CharField(max_length=255)
    mutuelle = models.CharField(max_length=100)
    personne_contact = models.CharField(max_length=255, null=True, blank=True)
    sexe = models.CharField(max_length=1, choices=SEXE_CHOICES)
    
    # Relation 1:1 avec l'utilisateur ayant le rôle patient
    patient = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, limit_choices_to={'role': 'patient'},related_name='dpi_as_patient')
    medecin_traitant = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, limit_choices_to={'role': 'medecin'},related_name='dpi_as_medecin_traitant',null=True, blank=True)

    def __str__(self):
        return f"DPI {self.nss}"

