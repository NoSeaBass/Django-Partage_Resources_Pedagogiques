from django import forms
from .models import Utilisateur, Etudiant, Ressource, Annonce
from administrateur.models import Classe, Module

class InscriptionUtilisateurForm(forms.ModelForm):
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)
    password_conf = forms.CharField(label="Confirmer le mot de passe", widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

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

class RessourceForm(forms.ModelForm):
    class Meta:
        model = Ressource
        fields = ['titre', 'module', 'fichier', 'description']
        widgets = {
            'titre': forms.TextInput(attrs={'class': 'form-control'}),
            'module': forms.Select(attrs={'class': 'form-select'}),
            'fichier': forms.FileInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        enseignant = kwargs.pop('enseignant', None)
        super().__init__(*args, **kwargs)
        if enseignant:
            self.fields['module'].queryset = Module.objects.filter(
                affectations__enseignant=enseignant
            ).distinct()

class AnnonceForm(forms.ModelForm):
    class Meta:
        model = Annonce
        fields = ['titre', 'classe', 'contenu']
        widgets = {
            'titre': forms.TextInput(attrs={'class': 'form-control'}),
            'classe': forms.Select(attrs={'class': 'form-select'}),
            'contenu': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        enseignant = kwargs.pop('enseignant', None)
        super().__init__(*args, **kwargs)
        if enseignant:
            classes_responsable_ids = enseignant.affectations.filter(
                est_responsable=True
            ).values_list('classe_id', flat=True)

            self.fields['classe'].queryset = Classe.objects.filter(
                id__in=classes_responsable_ids
            )

class ModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = ['intitule']
