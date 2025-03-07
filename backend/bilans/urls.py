from django.urls import path
from . import views

urlpatterns = [
    path('images-radiologiques/all/', views.getRadiologueImages, name='get_all_images_radiologiques'),
    path('analyses-biologiques/all/', views.getAllAnalysesBiologiques, name='get_all_analyses_biologiques'),
    path('images-radiologiques/', views.get_images_radiologiques, name='get_images_radiologiques'),
    path('analyses-biologiques/', views.get_analyses_biologiques, name='get_analyse_biologiques'),

    path('remplir-image-radiologique/', views.remplir_image_radiologique, name='remplir_image_radiologique'),
    path('remplir-analyse-biologique/', views.remplir_analyse_biologique, name='remplir-analyse-biologique'),
]
