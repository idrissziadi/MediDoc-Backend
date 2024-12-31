from rest_framework import permissions



class IsRadiologue(permissions.BasePermission):
    
    def has_permission(self, request, view):
        # Vérifie si l'utilisateur a un rôle "patient" ou "medecin"
        return request.user.is_authenticated and request.user.role in ['radiologue'] 