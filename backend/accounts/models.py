from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Crée et retourne un utilisateur avec un email, mot de passe, nom, role et specialite.
        """
        if not email:
            raise ValueError('L\'adresse email est obligatoire.')
        if not extra_fields.get('nom'):
            raise ValueError('Le champ "nom" est obligatoire.')
        if not extra_fields.get('role'):
            raise ValueError('Le champ "role" est obligatoire.')
        if not extra_fields.get('specialite'):
            raise ValueError('Le champ "specialite" est obligatoire.')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Crée et retourne un superutilisateur.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Le superutilisateur doit avoir is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Le superutilisateur doit avoir is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Modèle personnalisé pour les utilisateurs avec des rôles et spécialités.
    """
    # Champs de base
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

    # Champs supplémentaires
    ROLE_CHOICES = [
        ('patient', 'Patient'),
        ('medecin', 'Médecin'),
        ('radiologue', 'Radiologue'),
        ('laborantin', 'Laborantin'),
        ('infirmier', 'Infirmier'),
    ]
    role = models.CharField(max_length=15, choices=ROLE_CHOICES)

    SPECIALITY_CHOICES = [
        ('pediatre', 'Pédiatre'),
        ('cardiologue', 'Cardiologue'),
        ('ophtalmologue', 'Ophtalmologue'),
        ('neurologue', 'Neurologue'),
        ('other', 'Other'),
    ]
    specialite = models.CharField(max_length=20, choices=SPECIALITY_CHOICES)

    # Champs pour la gestion utilisateur
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nom', 'role', 'specialite']

    def __str__(self):
        return self.email
