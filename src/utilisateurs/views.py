from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import PersonneForm, InscriptionUtilisateurForm, EtudiantForm

def inscription_etudiant(request):
    if request.method == 'POST':
        # On récupère les données envoyées pour chaque formulaire
        personne_form = PersonneForm(request.POST)
        user_form = InscriptionUtilisateurForm(request.POST)
        etudiant_form = EtudiantForm(request.POST)

        # On vérifie si tous les formulaires sont valides
        if personne_form.is_valid() and user_form.is_valid() and etudiant_form.is_valid():
            # Sauvegarde dans l'ordre pour respecter les clés étrangères
            personne = personne_form.save()
            user = user_form.save(commit=False)
            user.save()

            etudiant = etudiant_form.save(commit=False)
            etudiant.personne = personne
            etudiant.utilisateur = user
            etudiant.save()

            messages.success(request, "Inscription réussie !")
            return redirect('nom_de_ta_page_accueil')
        else:
            messages.error(request, "Veuillez corriger les erreurs ci-dessous.")
    else:
        # Cas où la page est juste chargée (GET)
        personne_form = PersonneForm()
        user_form = InscriptionUtilisateurForm()
        etudiant_form = EtudiantForm()

    context = {
        'personne_form': personne_form,
        'user_form': user_form,
        'etudiant_form': etudiant_form,
    }
    return render(request, 'utilisateurs/etudiant/inscription.html', context)
