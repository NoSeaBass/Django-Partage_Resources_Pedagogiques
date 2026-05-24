from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class UtilisateurManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("L'email est obligatoire.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class Utilisateur(AbstractUser):
    ROLES = [
        ('ADMIN', 'Administrateur'),
        ('ENSEIGNANT', 'Enseignant'),
        ('ETUDIANT', 'Etudiant'),
    ]
    email = models.EmailField(unique=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    telephone = models.CharField(max_length=20, blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLES, default='ETUDIANT')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'prenom', 'nom']

    objects = UtilisateurManager()

    def __str__(self):
        return f"{self.prenom} {self.nom}"

    @property
    def is_etudiant(self):
        return self.role == 'ETUDIANT'

    @property
    def is_enseignant(self):
        return self.role == 'ENSEIGNANT'

class Enseignant(models.Model):
    utilisateur = models.OneToOneField(Utilisateur, on_delete=models.CASCADE, primary_key=True, related_name='profil_enseignant')
    grade = models.CharField(max_length=50, blank=True, null=True)

class Etudiant(models.Model):
    utilisateur = models.OneToOneField(Utilisateur, on_delete=models.CASCADE, primary_key=True, related_name='profil_etudiant')
    NCE = models.CharField(max_length=50, unique=True)
    classe = models.ForeignKey('administrateur.Classe', on_delete=models.SET_NULL, null=True, blank=True)