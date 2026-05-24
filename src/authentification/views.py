from django.shortcuts import render
from django.contrib.auth import login
from .forms import ConnexionForm

def page_accueil(request):
    return render(request, 'shared/acceuil.html')

def page_contact(request):
    return render(request, 'shared/contact.html')

def connexion_public(request):
    if request.method == 'POST':
        form = ConnexionForm(request.POST)
        if form.is_valid():
            login(request, form.user)
            return redirect('utilisateurs:dashboard')
        else:
            messages.error(request, "Veuillez vérifier vos identifiants.")
    else:
        form = ConnexionForm()

    return render(request, 'authentification/authentification.html', {'form': form})