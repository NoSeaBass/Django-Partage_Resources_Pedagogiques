from django.shortcuts import render, redirect
#from django.contrib import messages
from django.contrib.auth import login, logout
from .forms import ConnexionForm

def page_accueil(request):
    return render(request, 'shared/acceuil.html')

def page_contact(request):
    return render(request, 'shared/contact.html')

def connexion_public(request):
    msg = ""
    form = ConnexionForm() # Initialisation par défaut

    if request.method == 'POST':
        form = ConnexionForm(request.POST)
        if form.is_valid():
            user = form.user

            if user.is_etudiant and not user.etudiant_a_une_classe:
                msg = "Vous n'êtes pas rattaché à une classe."

            elif user.is_enseignant:
                profil = user.profil_enseignant_safe
                if not profil or not profil.affectations.exists():
                    msg = "Votre compte n'est rattaché à aucune classe."

            if not msg:
                login(request, user)
                return redirect('utilisateurs:home')

        else:
            msg = "Identifiants invalides."

    return render(request, 'authentification/authentification.html', {'form': form, 'msg': msg})


def deconnexion(request):
    logout(request)
    return redirect('authentification:connexion')
