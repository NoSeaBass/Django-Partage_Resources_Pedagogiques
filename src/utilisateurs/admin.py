from django.contrib import admin
from .models import Utilisateur, Enseignant, Etudiant

# Register your models here.

admin.site.register(Utilisateur)
admin.site.register(Enseignant)
admin.site.register(Etudiant)
