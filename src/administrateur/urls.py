from django.urls import path
from . import views

app_name = 'administrateur'

urlpatterns = [

    path('login/', views.admin_login, name='admin_login'),
    path("logout/", views.admin_logout, name="logout"),
    path('profil/', views.profil, name='admin_profil'),

    path('admin_dashboard/',                       views.dashboard,            name='admin_dashboard'),

    path('enseignants/',                     views.enseignants,           name='admin_enseignants'),
    path('enseignants/ajouter/',             views.enseignant_ajouter,    name='admin_enseignant_ajouter'),
    path('enseignants/<int:pk>/modifier/',   views.enseignant_modifier,   name='admin_enseignant_modifier'),
    path('enseignants/<int:pk>/supprimer/',  views.enseignant_supprimer,  name='admin_enseignant_supprimer'),

    path('classes/',                         views.classes,               name='admin_classes'),
    path('classes/ajouter/',                 views.classe_ajouter,        name='admin_classe_ajouter'),
    path('classes/<int:pk>/modifier/',       views.classe_modifier,       name='admin_classe_modifier'),
    path('classes/<int:pk>/supprimer/',      views.classe_supprimer,      name='admin_classe_supprimer'),

    path('comptes/',                         views.comptes,               name='admin_comptes'),
    path('comptes/<int:pk>/activer/',        views.compte_activer,        name='admin_compte_activer'),
    path('comptes/<int:pk>/supprimer/',      views.compte_supprimer,      name='admin_compte_supprimer'),

    path('affectations/',views.affectations, name='admin_affectations'),

    path('affectations/ajouter/',views.affectation_ajouter,name='admin_affectation_ajouter'),
   path( 'affectations/supprimer/<int:pk>/', views.affectation_supprimer, name='admin_affectation_supprimer'),
]
