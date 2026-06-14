from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

from core.models import Utilisateur, Enseignant, Etudiant, Administrateur, Classe, Affectation


def admin_login(request):
    msg = ""
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            user = form.get_user()
            if Administrateur.objects.filter(utilisateur=user).exists():
                login(request, user)
                return redirect("administrateur:admin_dashboard")
            else:
                msg = "Accès réservé aux administrateurs."
        else:
            msg = "Identifiants invalides."

    return render(request, "administrateur/login.html", {
        "form": form,
        "msg": msg
    })

def admin_logout(request):
    logout(request)
    return redirect("administrateur:admin_login")

login_url='administrateur:admin_login'
def dashboard(request):
    return render(request, "administrateur/dashboard.html", {
        "nb_etudiants"  : Etudiant.objects.count(),
        "nb_enseignants": Enseignant.objects.count(),
        "nb_classes"    : Classe.objects.count(),
        "nb_comptes"    : Utilisateur.objects.count(),
    })


@login_required(login_url='admin_login')
def enseignants(request):
    return render(request, "administrateur/enseignants.html", {
        "enseignants": Enseignant.objects.select_related('utilisateur').all()
    })


@login_required(login_url='admin_login')
def enseignant_ajouter(request):
    from .forms import EnseignantForm
    form = EnseignantForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Enseignant ajouté")
        return redirect("administrateur:admin_enseignants")
    return render(request, "administrateur/enseignant_form.html", {"form": form})


@login_required(login_url='admin_login')
def enseignant_modifier(request, pk):
    from .forms import EnseignantForm
    enseignant = get_object_or_404(Enseignant, pk=pk)
    u = enseignant.utilisateur
    initial = {
        'prenom'   : u.prenom,
        'nom'      : u.nom,
        'email'    : u.email,
        'telephone': u.telephone,
    }
    form = EnseignantForm(request.POST or None, initial=initial)
    if request.method == "POST" and form.is_valid():
        form.save(instance=enseignant)
        messages.success(request, "Enseignant modifié")
        return redirect("administrateur:admin_enseignants")
    return render(request, "administrateur/enseignant_form.html", {"form": form})


@login_required(login_url='admin_login')
def enseignant_supprimer(request, pk):
    enseignant = get_object_or_404(Enseignant, pk=pk)
    enseignant.delete()
    messages.success(request, "Enseignant supprimé")
    return redirect("administrateur:admin_enseignants")


@login_required(login_url='admin_login')
def classes(request):
    return render(request, "administrateur/classes.html", {
        "classes": Classe.objects.all()
    })


@login_required(login_url='admin_login')
def classe_ajouter(request):
    from .forms import ClasseForm
    form = ClasseForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Classe ajoutée")
        return redirect("administrateur:admin_classes")
       
    return render(request, "administrateur/classe_form.html", {"form": form})


@login_required(login_url='admin_login')
def classe_modifier(request, pk):
    from .forms import ClasseForm
    classe = get_object_or_404(Classe, pk=pk)
    form = ClasseForm(request.POST or None, instance=classe)
    if form.is_valid():
        form.save()
        messages.success(request, "Classe modifiée")
        return redirect("administrateur:admin_classes")
        
    return render(request, "administrateur/classe_form.html", {
        "form": form, "classe": classe
    })


@login_required(login_url='admin_login')
def classe_supprimer(request, pk):
    classe = get_object_or_404(Classe, pk=pk)
    classe.delete()
    messages.success(request, "Classe supprimée")
    return redirect("administrateur:admin_classes")
    


@login_required(login_url='admin_login')
def comptes(request):
    return render(request, "administrateur/comptes.html", {
        "comptes": Utilisateur.objects.all()
    })


@login_required(login_url='admin_login')
def compte_activer(request, pk):
    compte = get_object_or_404(Utilisateur, pk=pk)
    compte.is_active = not compte.is_active
    compte.save()
    return redirect("administrateur:admin_comptes")


@login_required(login_url='admin_login')
def compte_supprimer(request, pk):
    compte = get_object_or_404(Utilisateur, pk=pk)
    compte.delete()
    messages.success(request, "Compte supprimé")
    return redirect("administrateur:admin_comptes")


@login_required(login_url='admin_login')
def affectations(request):
    affectations = (
        Affectation.objects
        .select_related('enseignant__utilisateur', 'classe')
        .order_by('enseignant_id', 'classe_id')
        .distinct('enseignant_id', 'classe_id')
    )

    return render(
        request,
        "administrateur/affectation.html",
        {"affectations": affectations}
    )




@login_required(login_url='admin_login')
def affectation_ajouter(request):
    from .forms import AffectationForm

    form = AffectationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Classe affectée à l'enseignant avec succès.")
        return redirect("administrateur:admin_affectation")

    return render(
        request,
        "administrateur/affectation_form.html",
        {"form": form}
    )


@login_required(login_url='admin_login')
def affectation_ajouter(request):
    from .forms import AffectationForm
    form = AffectationForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Affectation enregistrée")
        return redirect("administrateur:admin_affectations")
    return render(request, "administrateur/affectation_form.html", {"form": form})

@login_required(login_url='admin_login')
def affectation_supprimer(request, pk):
    affectation = get_object_or_404(Affectation, pk=pk)

    Affectation.objects.filter(
        enseignant=affectation.enseignant
    ).delete()

    messages.success(
        request,
        "Toutes les affectations de cet enseignant ont été supprimées."
    )

    return redirect("administrateur:admin_affectations")

@login_required(login_url='admin_login')
def profil(request):
    admin = get_object_or_404(Administrateur, utilisateur=request.user)
    if request.method == "POST":
        u = request.user
        u.prenom    = request.POST.get("prenom", u.prenom)
        u.nom       = request.POST.get("nom", u.nom)
        u.email     = request.POST.get("email", u.email)
        u.telephone = request.POST.get("telephone", u.telephone)
        u.save()
        if request.FILES.get("photo"):
            admin.photo = request.FILES["photo"]
            admin.save()
        messages.success(request, "Profil mis à jour")
        return redirect("administrateur:admin_profil")
    return render(request, "administrateur/profil.html", {
        "admin": admin,
        "user" : request.user
    })
