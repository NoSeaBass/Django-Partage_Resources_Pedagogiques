from django.contrib import admin
from .models import Administrateur, Classe, Module, Affectation

# Register your models here.

admin.site.register(Administrateur)
admin.site.register(Classe)
admin.site.register(Module)
admin.site.register(Affectation)
