from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm

def page_accueil(request):
    return render(request, 'shared/acceuil.html')

def page_contact(request):
    return render(request, 'shared/contact.html')

def connexion_public(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Redirection vers la vue commune, peu importe le rôle
            return redirect('utilisateurs:dashboard')
        else:
            messages.error(request, "Identifiants invalides.")
    else:
        form = AuthenticationForm()

    return render(request, 'authentification/authentification.html', {'form': form})
