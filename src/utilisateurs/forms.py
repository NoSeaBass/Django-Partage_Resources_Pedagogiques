from django import forms
from .models import Utilisateur, Etudiant, Personne

class PersonneForm(forms.ModelForm):
    class Meta:
        model = Personne
        fields = ['nom', 'prenom', 'telephone', 'email']

class InscriptionUtilisateurForm(forms.ModelForm):
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)
    password_conf = forms.CharField(label="Confirmer le mot de passe", widget=forms.PasswordInput)

    class Meta:
        model = Utilisateur
        fields = ['email']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_conf = cleaned_data.get("password_conf")
        if password != password_conf:
            raise forms.ValidationError("Les mots de passe ne correspondent pas.")
        return cleaned_data

class EtudiantForm(forms.ModelForm):
    class Meta:
        model = Etudiant
        fields = ['NCE']
