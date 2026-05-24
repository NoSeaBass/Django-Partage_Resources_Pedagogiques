from django.urls import path
from . import views

app_name = 'authentification'

urlpatterns = [
    path('', views.page_accueil, name='accueil'),

    path('contact/', views.page_contact, name='contact'),
    path('connexion/', views.connexion_public, name='connexion'),
]
