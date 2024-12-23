from rest_framework import permissions

class IsMedecin(permissions.BasePermission):
    """
    Permission personnalisée qui permet d'autoriser uniquement les médecins.
    """
    def has_permission(self, request, view):

        return request.user and request.user.is_authenticated and request.user.role == 'medecin'
    
class IsAdministratif(permissions.BasePermission):
     
    def has_permission(self, request, view):

        return request.user and request.user.is_authenticated and request.user.role == 'administratif'    


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
