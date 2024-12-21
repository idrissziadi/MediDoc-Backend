from django.urls import path
from . import views

urlpatterns = [
    path('', views.obtenir_medicaments, name='obtenir_medicaments'),  # GET
    path('creer/', views.creer_medicament, name='creer_medicament'),  # POST
    path('supprimer/<int:id_medicament>/', views.supprimer_medicament, name='supprimer_medicament'),  # DELETE
]
