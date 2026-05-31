from django.urls import path
from . import views

app_name = 'utilisateurs'

urlpatterns = [
    path('inscription/', views.inscription_etudiant, name='inscription_etudiant'),
    path('home/', views.home, name='home'),
    path('mon_profil', views.mon_profil, name='mon_profil'),
    path('modules/', views.modules, name='modules'),
    path('traitement_global/', views.traitement_global, name='traitement_global'),
    path('list_ressources/<int:module_id>/', views.list_ressources, name='list_ressources'),
    path('telecharger/<int:ressource_id>/', views.telecharger_ressource, name='telecharger_ressource'),
    path('historique/', views.historique_etudiants, name='historique_etudiants'),
    path('gestion-classe/<int:classe_id>/', views.gestion_classe, name='gestion_classe'),
]
