from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import InscriptionUtilisateurForm, EtudiantForm

def inscription_etudiant(request):
    if request.method == 'POST':
        user_form = InscriptionUtilisateurForm(request.POST)
        etudiant_form = EtudiantForm(request.POST)

        if user_form.is_valid() and etudiant_form.is_valid():
            user = user_form.save(commit=False)
            user.role = 'ETUDIANT'
            user.save()

            etudiant = etudiant_form.save(commit=False)
            etudiant.utilisateur = user
            etudiant.save()

            messages.success(request, "Inscription réussie !")
            return redirect('utilisateurs:home')
        else:
            messages.error(request, "Veuillez corriger les erreurs ci-dessous.")
    else:
        user_form = InscriptionUtilisateurForm()
        etudiant_form = EtudiantForm()

    context = {
        'user_form': user_form,
        'etudiant_form': etudiant_form,
    }
    return render(request, 'utilisateurs/etudiant/inscription.html', context)

def home(request):
    return render(request, 'utilisateurs/home.html')