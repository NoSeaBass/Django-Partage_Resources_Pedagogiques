from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from .forms import ConnexionForm

def page_accueil(request):
    return render(request, 'shared/acceuil.html')

def page_contact(request):
    return render(request, 'shared/contact.html')

def connexion_public(request):
    if request.method == 'POST':
        form = ConnexionForm(request.POST)
        if form.is_valid():
            user = form.user

            # 1. Vérification pour les étudiants
            if user.is_etudiant:
                if not user.etudiant_a_une_classe: # Ton property existant
                    messages.warning(request, "Vous n'êtes pas rattaché à une classe.")
                    return render(request, 'authentification/authentification.html', {'form': form})

            # 2. Vérification pour les enseignants
            elif user.is_enseignant:
                # On vérifie s'il existe au moins une affectation pour cet enseignant
                profil = user.profil_enseignant_safe
                if not profil or not profil.affectations.exists():
                    messages.warning(request, "Votre compte n'est rattaché à aucune classe.")
                    return render(request, 'authentification/authentification.html', {'form': form})

            # Si tout est OK, on connecte
            login(request, user)
            return redirect('utilisateurs:home')

        else:
            messages.error(request, "Identifiants invalides.")
    else:
        form = ConnexionForm()
    return render(request, 'authentification/authentification.html', {'form': form})


def deconnexion(request):
    logout(request)
    return redirect('authentification:connexion')
