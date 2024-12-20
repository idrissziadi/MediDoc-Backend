from django.urls import path
from . import views

urlpatterns = [
    # Endpoint pour ajouter un soin
    path('ajouter/', views.ajouterSoins, name='ajouter-soins'),
    path('supprimer/<int:soin_id>/', views.supprimerSoin, name='supprimer_soin'),
    path('dpi/<int:dpi_id>/', views.get_soins_par_dpi, name='get_soins_par_dpi'),  # Modification ici
]
