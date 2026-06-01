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
            login(request, user)

            if user.is_etudiant:

                if not user.etudiant_a_une_classe:

                    logout(request)
                    messages.warning(request, "Votre compte est bien activé, mais vous n'êtes pas encore rattaché à une classe. Contactez l'administration.")

                    return render(request, 'authentification/authentification.html', {'form': form})
                return redirect('utilisateurs:home')
            elif user.is_enseignant:
                return redirect('utilisateurs:home')
        else:
            messages.error(request, "Veuillez vérifier vos identifiants.")
    else:
        form = ConnexionForm()

    return render(request, 'authentification/authentification.html', {'form': form})

def deconnexion(request):
    logout(request)
    return redirect('authentification:connexion')
