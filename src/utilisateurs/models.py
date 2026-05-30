from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class UtilisateurManager(BaseUserManager):
    username = None
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
        ('ADMIN',        'Administrateur'),
        ('ENSEIGNANT',   'Enseignant'),
        ('RESPONSABLE',  'Responsable de classe'),
        ('ETUDIANT',     'Etudiant'),
    ]

    email     = models.EmailField(unique=True)
    nom       = models.CharField(max_length=100)
    prenom    = models.CharField(max_length=100)
    telephone = models.CharField(max_length=20, blank=True, null=True)
    role      = models.CharField(max_length=20, choices=ROLES, default='ETUDIANT')

    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = ['username', 'prenom', 'nom']

    objects = UtilisateurManager()

    def __str__(self):
        return f"{self.prenom} {self.nom} ({self.email})"

    # Proprietes de commodite — evite les requetes supplementaires dans les vues
    @property
    def is_admin(self):
        return self.role == 'ADMIN'

    @property
    def is_enseignant(self):
        return self.role in ('ENSEIGNANT', 'RESPONSABLE')

    @property
    def is_responsable(self):
        return self.role == 'RESPONSABLE'

    @property
    def is_etudiant(self):
        return self.role == 'ETUDIANT'

    @property
    def etudiant_a_une_classe(self):
        return self.is_etudiant and hasattr(self, 'profil_etudiant') and self.profil_etudiant.classe is not None

class Enseignant(models.Model):
    utilisateur = models.OneToOneField(Utilisateur, on_delete=models.CASCADE, primary_key=True, related_name='profil_enseignant')
    grade = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"Pr. {self.utilisateur.nom} {self.utilisateur.prenom}"

class Etudiant(models.Model):
    utilisateur = models.OneToOneField(Utilisateur, on_delete=models.CASCADE, primary_key=True, related_name='profil_etudiant')
    NCE = models.CharField(max_length=50, unique=True)
    classe = models.ForeignKey('administrateur.Classe', on_delete=models.SET_NULL, null=True, blank=True)

class Ressource(models.Model):
    titre       = models.CharField(max_length=150)
    fichier     = models.FileField(upload_to='ressources/')
    description = models.TextField(blank=True, null=True)
    date_ajout  = models.DateTimeField(auto_now_add=True)
    module      = models.ForeignKey('administrateur.Module', on_delete=models.CASCADE, related_name='ressources')
    enseignant  = models.ForeignKey(Enseignant, on_delete=models.CASCADE, related_name='ressources_publiees')

    def __str__(self):
        return self.titre


class Annonce(models.Model):
    titre         = models.CharField(max_length=150)
    contenu       = models.TextField()
    date_datetime = models.DateTimeField(auto_now_add=True)
    classe        = models.ForeignKey('administrateur.Classe', on_delete=models.CASCADE, related_name='annonces')
    enseignant    = models.ForeignKey(Enseignant, on_delete=models.CASCADE, related_name='annonces_publiees')

    def __str__(self):
        return self.titre


class Notification(models.Model):
    titre         = models.CharField(max_length=150)
    message       = models.TextField()
    lue           = models.BooleanField(default=False)
    date_datetime = models.DateTimeField(auto_now_add=True)
    etudiant      = models.ForeignKey(Etudiant, on_delete=models.CASCADE, related_name='notifications')

    def __str__(self):
        return f"Notification pour {self.etudiant.NCE} : {self.titre}"


class Historique(models.Model):
    ACTIONS_CHOICES = [
        ('telechargement', 'Telechargement'),
        ('consultation',   'Consultation'),
    ]
    action        = models.CharField(max_length=50, choices=ACTIONS_CHOICES)
    date_datetime = models.DateTimeField(auto_now_add=True)
    ressource = models.ForeignKey('Ressource', on_delete=models.CASCADE, related_name='historiques', null=True, blank=True)
    etudiant      = models.ForeignKey(Etudiant, on_delete=models.CASCADE, related_name='historiques')

    def __str__(self):
        return f"{self.etudiant.NCE} - {self.action} ({self.date_datetime})"


    def __str__(self):
        return self.intitule
