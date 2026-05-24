from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Personne(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    telephone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.prenom} {self.nom}"

from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models

class Utilisateur(AbstractUser):
    email = models.EmailField(unique=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    telephone = models.CharField(max_length=20, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'prenom', 'nom']

    objects = UserManager()

    def __str__(self):
        return f"{self.prenom} {self.nom} ({self.email})"

class Enseignant(models.Model):
    utilisateur = models.OneToOneField(Utilisateur, on_delete=models.CASCADE, primary_key=True, related_name='profil_enseignant')
    grade = models.CharField(max_length=50, blank=True, null=True)
    specialite = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Pr. {self.utilisateur.nom} {self.utilisateur.prenom}"

class Etudiant(models.Model):
    utilisateur = models.OneToOneField(Utilisateur, on_delete=models.CASCADE, primary_key=True, related_name='profil_etudiant')
    NCE = models.CharField(max_length=50, unique=True)
    # Note : Le lien avec Classe se fera via un import ou restera générique si Classe bouge
    classe = models.ForeignKey('administrateur.Classe', on_delete=models.SET_NULL, null=True, blank=True, related_name='etudiants')

    def __str__(self):
        return f"Etudiant: {self.NCE}"
