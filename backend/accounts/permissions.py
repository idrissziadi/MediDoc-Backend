from rest_framework import permissions

class IsMedecin(permissions.BasePermission):
    """
    Permission personnalisée qui permet d'autoriser uniquement les médecins.
    """
    def has_permission(self, request, view):
        # Vérifie si l'utilisateur est authentifié et si son rôle est "doctor"
        return request.user and request.user.role == 'medecin'

class IsAdministratif(permissions.BasePermission):
     
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False         
        role = getattr(request.user, 'role', None)   
        if role == 'administratif':
            return True   
        return False
    
class IsMedecinOrAdministratif(permissions.BasePermission):
    """
    Permission personnalisée qui permet d'autoriser uniquement les médecins et les administratifs.
    """
    def has_permission(self, request, view):
        # Vérifie si l'utilisateur est authentifié et si son rôle est "doctor"
        return request.user and (request.user.role == 'medecin' or request.user.role == 'administratif')