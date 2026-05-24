from django.db import models
from utilisateurs.models import Utilisateur, Enseignant

# Create your models here.


class Administrateur(models.Model):
    utilisateur = models.OneToOneField(Utilisateur, on_delete=models.CASCADE, primary_key=True, related_name='profil_admin')
    niveau_ces = models.IntegerField()

    def __str__(self):
        return f"Admin: {self.utilisateur.email}"

class Classe(models.Model):
    nom = models.CharField(max_length=50)
    effectif = models.IntegerField(default=0)
    annee = models.IntegerField()

    def __str__(self):
        return f"{self.nom} ({self.annee})"

class Module(models.Model):
    intitule = models.CharField(max_length=150)
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE, related_name='modules')

    def __str__(self):
        return self.intitule

class Affectation(models.Model):
    enseignant = models.ForeignKey(Enseignant, on_delete=models.CASCADE, related_name='affectations')
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE, related_name='affectations')
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='affectations')
    est_responsable = models.BooleanField(default=False)
    date_debut = models.DateTimeField()
    date_fin = models.DateTimeField()

    def __str__(self):
        role = "Responsable" if self.est_responsable else "Intervenant"
        return f"{self.enseignant} - {self.module.intitule} ({role})"
