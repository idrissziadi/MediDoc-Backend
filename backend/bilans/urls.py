from django.urls import path
from . import views

urlpatterns = [
    path('images-radiologiques/', views.get_images_radiologiques, name='get_images_radiologiques'),
    path('analyses-biologiques/', views.get_analyses_biologiques, name='get_analyse_biologiques'),
]
