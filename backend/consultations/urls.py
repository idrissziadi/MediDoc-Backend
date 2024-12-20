from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_all_consultations, name='get_all_consultations'),            # Liste des consultations
    path('<int:id_consultation>/', views.get_consultation_by_id, name='get_consultation_by_id'),  # Consultation par ID
    path('creer/', views.create_consultation, name='create_consultation'),         # Créer une consultation
    path('<int:id_consultation>/modifier/', views.update_consultation, name='update_consultation'), # Mise à jour
    path('<int:id_consultation>/supprimer/', views.delete_consultation, name='delete_consultation'), # Suppression
]
