from rest_framework import permissions

class IsInfirmier(permissions.BasePermission):
    """
    Permission personnalisée pour vérifier si l'utilisateur est infirmier.
    """
    def has_permission(self, request, view):
        # L'utilisateur doit être authentifié et avoir un rôle 'infirmier'
        return request.user.is_authenticated and request.user.role == 'infirmier'

class IsPatientOrMedecinOrInfirmier(permissions.BasePermission):
    """
    Permission personnalisée pour vérifier si l'utilisateur est patient, médecin ou infirmier.
    """
    def has_permission(self, request, view):
        # L'utilisateur doit être authentifié et avoir un rôle 'patient', 'medecin' ou 'infirmier'
        return request.user.is_authenticated and request.user.role in ['patient', 'medecin', 'infirmier']