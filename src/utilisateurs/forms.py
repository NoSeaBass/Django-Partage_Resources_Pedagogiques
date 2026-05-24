from django import forms
from .models import Utilisateur, Etudiant

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