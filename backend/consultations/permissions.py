from rest_framework import permissions

class IsMedecin(permissions.BasePermission):
    """
    Permission personnalisée qui permet d'autoriser uniquement les médecins.
    """
    def has_permission(self, request, view):
        # Vérifie si l'utilisateur est authentifié et si son rôle est "doctor"
        return request.user and request.user.role == 'medecin'
