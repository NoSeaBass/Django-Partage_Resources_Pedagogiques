from django.urls import path
from . import views

app_name = 'utilisateurs'

urlpatterns = [
    path('inscription/', views.inscription_etudiant, name='inscription_etudiant'),
    path('home/', views.home, name='home'),
    path('modules/', views.modules, name='modules'),
    path('traitement_global/', views.traitement_global, name='traitement_global'),
    path('list_ressources/<int:module_id>/', views.list_ressources, name='list_ressources'),
]
