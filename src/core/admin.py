from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    Utilisateur, Classe, Administrateur, Enseignant,
    Etudiant, Module, Affectation, Ressource, Annonce
)

@admin.register(Utilisateur)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'nom', 'prenom', 'role', 'get_profil_nce')
    list_filter = ('role', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        ('Informations Complémentaires', {'fields': ('role', 'telephone')}),
    )

    def get_profil_nce(self, obj):
        if obj.role == 'ETUDIANT' and hasattr(obj, 'profil_etudiant'):
            return obj.profil_etudiant.NCE
        return "-"
    get_profil_nce.short_description = 'NCE Etudiant'

@admin.register(Classe)
class ClasseAdmin(admin.ModelAdmin):
    list_display = ('nom', 'annee', 'get_effectif')
    search_fields = ('nom',)

    def get_effectif(self, obj):
        return obj.etudiant_set.count()
    get_effectif.short_description = 'Effectif'

@admin.register(Affectation)
class AffectationAdmin(admin.ModelAdmin):
    list_display = ('enseignant', 'classe', 'module', 'est_responsable')
    list_filter = ('classe', 'est_responsable')
    list_select_related = ('enseignant', 'classe', 'module')

@admin.register(Ressource)
class RessourceAdmin(admin.ModelAdmin):
    list_display = ('titre', 'module', 'enseignant', 'date_ajout')
    list_filter = ('module__classe', 'date_ajout')
    search_fields = ('titre', 'description')
    date_hierarchy = 'date_ajout'

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('intitule', 'classe')
    list_filter = ('classe',)

@admin.register(Administrateur)
class AdministrateurAdmin(admin.ModelAdmin):
    list_display = ('utilisateur',)

@admin.register(Enseignant)
class EnseignantAdmin(admin.ModelAdmin):
    list_display = ('__str__',)

@admin.register(Etudiant)
class EtudiantAdmin(admin.ModelAdmin):
    list_display = ('utilisateur', 'NCE', 'classe')
    search_fields = ('NCE', 'utilisateur__nom')

@admin.register(Annonce)
class AnnonceAdmin(admin.ModelAdmin):
    list_display = ('titre', 'classe', 'enseignant', 'date_datetime')
    list_filter = ('classe', 'date_datetime')
