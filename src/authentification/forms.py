from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate

class ConnexionForm(forms.Form):
    email = forms.EmailField(label="Adresse email")
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        
        if email and password:
            self.user = authenticate(username=email, password=password)
            if self.user is None:
                raise forms.ValidationError("Email ou mot de passe incorrect.")
        return self.cleaned_data