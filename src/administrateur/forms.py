from django import forms
from datetime import date
from django.contrib.auth.hashers import make_password
from core.models import Utilisateur, Etudiant, Enseignant, Classe, Affectation



class InscriptionUtilisateurForm(forms.ModelForm):
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)
    password_conf = forms.CharField(label="Confirmer le mot de passe", widget=forms.PasswordInput)

    class Meta:
        model = Utilisateur
        fields = ['email', 'nom', 'prenom', 'telephone']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_conf = cleaned_data.get("password_conf")
        if password and password_conf and password != password_conf:
            raise forms.ValidationError("Les mots de passe ne correspondent pas.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.role = 'ETUDIANT'
        if commit:
            user.save()
        return user

class EtudiantForm(forms.ModelForm):
    class Meta:
        model = Etudiant
        fields = ['NCE']


#  Enseignant

class EnseignantForm(forms.Form):
    prenom     = forms.CharField(max_length=100, label="Prénom")
    nom        = forms.CharField(max_length=100, label="Nom")
    email      = forms.EmailField(label="Email")
    telephone  = forms.CharField(max_length=20, required=False, label="Téléphone")
    password   = forms.CharField(widget=forms.PasswordInput, required=False, label="Mot de passe")

    def save(self, instance=None):
        data = self.cleaned_data
        if instance:
            u = instance.utilisateur
            u.prenom, u.nom, u.email, u.telephone = data['prenom'], data['nom'], data['email'], data['telephone']
            if data['password']:
                u.set_password(data['password'])
            u.save()
            return instance
        else:
            u = Utilisateur.objects.create(
                prenom=data['prenom'], nom=data['nom'], email=data['email'],
                username=data['email'], telephone=data['telephone'], role='ENSEIGNANT'
            )
            u.set_password(data['password'] or 'changeme123')
            u.save()
            return Enseignant.objects.create(utilisateur=u)


#  Classe 

class ClasseForm(forms.ModelForm):
    class Meta:
        model  = Classe
        fields = ['nom', 'annee']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.initial.get('annee'):
            self.initial['annee'] = date.today().year


#  Affectation

class AffectationForm(forms.ModelForm):
    class Meta:
        model   = Affectation
        fields  = ['enseignant', 'classe', 'est_responsable', 'date_debut', 'date_fin']
        widgets = {
            'date_debut': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'date_fin'  : forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

        
