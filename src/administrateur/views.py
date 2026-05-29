from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import Administrateur



def admin_login(request):

    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST":

        if form.is_valid():

            user = form.get_user()

            # Vérifie si l'utilisateur est administrateur
            if Administrateur.objects.filter(utilisateur=user).exists():

                login(request, user)

                return redirect("admin_dashboard")

            else:
                messages.error(request, "Accès réservé aux administrateurs.")

        else:
            messages.error(request, "Identifiants invalides.")

    return render(request, "administrateur/login.html", {
        "form": form
    })



# DASHBOARD


def dashboard(request):

    from etudiant.models import Utilisateur, Etudiant, Classe
    from enseignant.models import Enseignant

    context = {
        "nb_etudiants": Etudiant.objects.count(),
        "nb_enseignants": Enseignant.objects.count(),
        "nb_classes": Classe.objects.count(),
        "nb_comptes": Utilisateur.objects.count(),
    }

    return render(request, "administrateur/dashboard.html", context)


# LISTE DES ENSEIGNANTS
def enseignants(request):

    from enseignant.models import Enseignant

    enseignants = Enseignant.objects.all()

    return render(request, "administrateur/enseignants.html", {
        "enseignants": enseignants
    })



# AJOUTER ENSEIGNANT


def enseignant_ajouter(request):

    from enseignant.forms import EnseignantForm

    form = EnseignantForm(request.POST or None)

    if form.is_valid():

        form.save()

        messages.success(request, "Enseignant ajouté")

        return redirect("admin_enseignants")

    return render(request, "administrateur/enseignant_form.html", {
        "form": form
    })



# MODIFIER ENSEIGNANT


def enseignant_modifier(request, pk):

    from enseignant.models import Enseignant
    from enseignant.forms import EnseignantForm

    enseignant = get_object_or_404(Enseignant, pk=pk)

    form = EnseignantForm(request.POST or None, instance=enseignant)

    if form.is_valid():

        form.save()

        messages.success(request, "Enseignant modifié")

        return redirect("admin_enseignants")

    return render(request, "administrateur/enseignant_form.html", {
        "form": form
    })



# SUPPRIMER ENSEIGNANT


def enseignant_supprimer(request, pk):

    from enseignant.models import Enseignant

    enseignant = get_object_or_404(Enseignant, pk=pk)

    enseignant.delete()

    messages.success(request, "Enseignant supprimé")

    return redirect("admin_enseignants")



# CLASSES


def classes(request):

    from etudiant.models import Classe

    classes = Classe.objects.all()

    return render(request, "administrateur/classes.html", {
        "classes": classes
    })

# AJOUTER CLASSE
def classe_ajouter(request):

    from etudiant.forms import ClasseForm

    form = ClasseForm(request.POST or None)

    if form.is_valid():

        form.save()

        messages.success(request, "Classe ajoutée")

        return redirect("admin_classes")

    return render(request, "administrateur/classe_form.html", {
        "form": form
    })


# SUPPRIMER CLASSE

def classe_supprimer(request, pk):

    from etudiant.models import Classe

    classe = get_object_or_404(Classe, pk=pk)

    classe.delete()

    messages.success(request, "Classe supprimée")

    return redirect("admin_classes")



# COMPTES


def comptes(request):

    from etudiant.models import Utilisateur

    comptes = Utilisateur.objects.all()

    return render(request, "administrateur/comptes.html", {
        "comptes": comptes
    })



# ACTIVER / DÉSACTIVER


def compte_activer(request, pk):

    from etudiant.models import Utilisateur

    compte = get_object_or_404(Utilisateur, pk=pk)

    compte.is_active = not compte.is_active

    compte.save()

    return redirect("admin_comptes")



# SUPPRIMER COMPTE


def compte_supprimer(request, pk):

    from etudiant.models import Utilisateur

    compte = get_object_or_404(Utilisateur, pk=pk)

    compte.delete()

    messages.success(request, "Compte supprimé")

    return redirect("admin_comptes")



# ÉTUDIANTS


def etudiants(request):

    from etudiant.models import Etudiant

    etudiants = Etudiant.objects.all()

    return render(request, "administrateur/etudiants.html", {
        "etudiants": etudiants
    })


# PROFIL


def profil(request):

    return render(request, "administrateur/profil.html")



# INSCRIPTION


def register(request):

    form = UserCreationForm(request.POST or None)

    if form.is_valid():

        form.save()

        messages.success(request, "Compte créé")

        return redirect("login")

    return render(request, "register.html", {
        "form": form
    })


def profil(request):
    from .models import Administrateur

    admin = get_object_or_404(Administrateur, utilisateur=request.user)

    return render(request, "administrateur/profil.html", {
        "admin": admin,
        "user": request.user
    })