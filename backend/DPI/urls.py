from django.urls import path
from . import views

urlpatterns = [
    path('creer/', views.creer_dpi, name='creer_dpi'),
    path('consulter/<str:nss>/', views.consulter_dpi, name='consulter_dpi'),
    path('rechercher/<str:nss>/', views.rechercher_dpi_par_nss, name='rechercher_dpi_par_nss'),
    path('modifier/<int:dpi_id>/', views.modifier_dpi, name='modifier_dpi'),
    path('supprimer/<str:dpi_id>/', views.supprimer_dpi, name='supprimer_dpi'),
]
