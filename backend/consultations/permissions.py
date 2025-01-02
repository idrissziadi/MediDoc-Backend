from rest_framework import permissions

class IsMedecin(permissions.BasePermission):
    """
    Permission personnalisée qui permet d'autoriser uniquement les médecins.
    """
    def has_permission(self, request, view):
        # Vérifie si l'utilisateur est authentifié et si son rôle est "doctor"
        return request.user and request.user.role == 'medecin'

class IsPatientOrMedecin(permissions.BasePermission):
    """
    Permission personnalisée pour autoriser les patients et les médecins.
    """
    def has_permission(self, request, view):
        # Vérifie si l'utilisateur a un rôle "patient" ou "medecin"
        return request.user.is_authenticated and request.user.role in ['patient', 'medecin'] 