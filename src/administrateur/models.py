from django.db import models
from utilisateurs.models import Utilisateur, Enseignant


# ── Administrateur ──────────────────────────────────────────

class Administrateur(models.Model):
    utilisateur = models.OneToOneField(
        Utilisateur,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='profil_admin'
    )
    niveau_ces = models.IntegerField()
    telephone  = models.CharField(max_length=20, blank=True)
    photo      = models.ImageField(upload_to='admins/', blank=True, null=True)

    def __str__(self):
        return f"Admin: {self.utilisateur.email}"


# ── Classe ──────────────────────────────────────────────────

class Classe(models.Model):
    nom      = models.CharField(max_length=50)
    effectif = models.IntegerField(default=0)
    annee    = models.IntegerField()

    def __str__(self):
        return f"{self.nom} ({self.annee})"


# ── Module ──────────────────────────────────────────────────

class Module(models.Model):
    intitule = models.CharField(max_length=150)
    classe   = models.ForeignKey(
        Classe,
        on_delete=models.CASCADE,
        related_name='modules'
    )

    def __str__(self):
        return self.intitule


# ── Affectation ─────────────────────────────────────────────

class Affectation(models.Model):
    enseignant      = models.ForeignKey(
        Enseignant,
        on_delete=models.CASCADE,
        related_name='affectations'
    )
    classe          = models.ForeignKey(
        Classe,
        on_delete=models.CASCADE,
        related_name='affectations'
    )

    # ✅ nullable : géré par le prof responsable, pas l'admin
    module          = models.ForeignKey(
        Module,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='affectations'
    )

    est_responsable = models.BooleanField(default=False)
    date_debut      = models.DateTimeField()
    date_fin        = models.DateTimeField()

    class Meta:
        unique_together = ('enseignant', 'classe')

    def __str__(self):
        role = "Responsable" if self.est_responsable else "Intervenant"
        module_str = self.module.intitule if self.module else "Aucun module"
        return f"{self.enseignant} - {module_str} ({role})"