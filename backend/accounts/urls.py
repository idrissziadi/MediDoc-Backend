from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('user/<int:user_id>/', views.get_user, name='get_user'),  # URL pour rechercher un utilisateur
    path('medecins/', views.get_medecins, name='get_medecins'),
]
