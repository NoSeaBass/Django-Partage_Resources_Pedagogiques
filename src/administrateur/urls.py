from django.urls import path
from . import views

app_name = 'administrateur'

urlpatterns = [

    path('login/', views.admin_login, name='admin_login'),
    path('profil/', views.profil, name='admin_profil'),
    # Dashboard
    path('dashboard/',                       views.dashboard,            name='admin_dashboard'),

    # Enseignants
    path('enseignants/',                     views.enseignants,           name='admin_enseignants'),
    path('enseignants/ajouter/',             views.enseignant_ajouter,    name='admin_enseignant_ajouter'),
    path('enseignants/<int:pk>/modifier/',   views.enseignant_modifier,   name='admin_enseignant_modifier'),
    path('enseignants/<int:pk>/supprimer/',  views.enseignant_supprimer,  name='admin_enseignant_supprimer'),

    # Classes
    path('classes/',                         views.classes,               name='admin_classes'),
    path('classes/ajouter/',                 views.classe_ajouter,        name='admin_classe_ajouter'),
    path('classes/<int:pk>/modifier/',       views.classe_modifier,       name='admin_classe_modifier'),
    path('classes/<int:pk>/supprimer/',      views.classe_supprimer,      name='admin_classe_supprimer'),

    # Comptes
    path('comptes/',                         views.comptes,               name='admin_comptes'),
    path('comptes/<int:pk>/activer/',        views.compte_activer,        name='admin_compte_activer'),
    path('comptes/<int:pk>/supprimer/',      views.compte_supprimer,      name='admin_compte_supprimer'),

    # Étudiants
    path('etudiants/',                       views.etudiants,             name='admin_etudiants'),
]
