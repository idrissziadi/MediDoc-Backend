from django.urls import path
from . import views

urlpatterns = [
    path('creer/', views.creer_dpi, name='creer_dpi'),
    path('consulter/', views.consulter_dpi, name='consulter_dpi'),
    path('rechercher/<str:nss>/', views.rechercher_dpi_par_nss, name='rechercher_dpi_par_nss'),
    path('consulter-qr/<str:qr_code>/', views.consulter_dpi_par_qr, name='consulter_dpi_par_qr'),
]
