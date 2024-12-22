from rest_framework import permissions

class IsMedecin(permissions.BasePermission):
    """
    Permission personnalisée qui permet d'autoriser uniquement les médecins.
    """
    def has_permission(self, request, view):
        # Si l'utilisateur n'est pas authentifié
        if not request.user.is_authenticated:
            # Vous pouvez autoriser ou refuser les utilisateurs anonymes ici
            return False  # Bloque l'accès aux utilisateurs non authentifiés

        # Si l'utilisateur est authentifié, vérifiez son rôle
        role = getattr(request.user, 'role', None)  # Retourne None si 'role' n'existe pas

        # Définissez la logique pour vérifier les rôles
        if role == 'medecin':
            return True  # Accès autorisé pour les médecins

        return False
    
class IsAdministratif(permissions.BasePermission):
     
    def has_permission(self, request, view):
        # Si l'utilisateur n'est pas authentifié
        if not request.user.is_authenticated:
            # Vous pouvez autoriser ou refuser les utilisateurs anonymes ici
            return False  # Bloque l'accès aux utilisateurs non authentifiés

        # Si l'utilisateur est authentifié, vérifiez son rôle
        role = getattr(request.user, 'role', None)  # Retourne None si 'role' n'existe pas

        # Définissez la logique pour vérifier les rôles
        if role == 'administratif':
            return True  # Accès autorisé pour les médecins

        return False    


class IsPatient(permissions.BasePermission):
    """
    Permission personnalisée qui permet d'autoriser uniquement les patients.
    """
    def has_permission(self, request, view):
        # Vérifie si l'utilisateur est authentifié et si son rôle est "patient"
        return request.user and request.user.role == 'patient'

class IsInfirmier(permissions.BasePermission):
    """
    Permission personnalisée qui permet d'autoriser uniquement les patients.
    """
    def has_permission(self, request, view):
        print("User:", request.user)
        print("Role:", request.user.role)
        # Vérifie si l'utilisateur est authentifié et si son rôle est "patient"
        return request.user and request.user.role == 'infirmier'        


from rest_framework import permissions

class IsMedecinOrInfirmier(permissions.BasePermission):
    """
    Permission personnalisée pour autoriser uniquement les médecins et infirmiers.
    """
    def has_permission(self, request, view):
        # Vérifie si l'utilisateur a un rôle "medecin" ou "infirmier"
        return request.user and request.user.is_authenticated and request.user.role in ['medecin', 'infirmier']
