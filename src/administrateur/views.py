from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages

from django.contrib.auth import authenticate, login

from .models import Administrateur

# Coucou Diarra, j'ai ajouter ce formulaire provenant du formulaire depuis une sorte d'association

from django.contrib.auth.forms import AuthenticationForm

def admin_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()

            if Administrateur.objects.filter(utilisateur=user).exists():
                login(request, user)
                return redirect('administrateur:admin_dashboard')
            else:
                messages.error(request, "Accès réservé aux administrateurs.")
        else:
            messages.error(request, "Identifiants invalides.")
    else:
        form = AuthenticationForm()

    return render(request, 'administrateur/login.html', {'form': form})




def is_admin(user):
    return user.is_authenticated and user.is_staff

# ── DASHBOARD ──
@login_required
@user_passes_test(is_admin)
def dashboard(request):
    from etudiant.models import Utilisateur, Etudiant, Classe
    from enseignant.models import Enseignant
    context = {
        'nb_etudiants'    : Etudiant.objects.count(),
        'nb_enseignants'  : Enseignant.objects.count(),
        'nb_classes'      : Classe.objects.count(),
        'nb_comptes'      : Utilisateur.objects.count(),
        'derniers_comptes': Utilisateur.objects.order_by('-date_joined')[:5],
    }
    return render(request, 'administrateur/dashboard.html', context)

# ── ENSEIGNANTS ──
@login_required
@user_passes_test(is_admin)
def enseignants(request):
    from enseignant.models import Enseignant
    return render(request, 'administrateur/enseignants.html', {
        'enseignants': Enseignant.objects.all()
    })

@login_required
@user_passes_test(is_admin)
def enseignant_ajouter(request):
    from enseignant.forms import EnseignantForm
    form = EnseignantForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Enseignant ajouté.")
        return redirect('admin_enseignants')
    return render(request, 'administrateur/enseignant_form.html', {'form': form, 'action': 'Ajouter'})

@login_required
@user_passes_test(is_admin)
def enseignant_modifier(request, pk):
    from enseignant.models import Enseignant
    from enseignant.forms import EnseignantForm
    obj = get_object_or_404(Enseignant, pk=pk)
    form = EnseignantForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        messages.success(request, "Enseignant modifié.")
        return redirect('admin_enseignants')
    return render(request, 'administrateur/enseignant_form.html', {'form': form, 'action': 'Modifier'})

@login_required
@user_passes_test(is_admin)
def enseignant_supprimer(request, pk):
    from enseignant.models import Enseignant
    get_object_or_404(Enseignant, pk=pk).delete()
    messages.success(request, "Enseignant supprimé.")
    return redirect('admin_enseignants')

# ── CLASSES ──
@login_required
@user_passes_test(is_admin)
def classes(request):
    from etudiant.models import Classe
    return render(request, 'administrateur/classes.html', {
        'classes': Classe.objects.all()
    })

@login_required
@user_passes_test(is_admin)
def classe_ajouter(request):
    from etudiant.forms import ClasseForm
    form = ClasseForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Classe ajoutée.")
        return redirect('admin_classes')
    return render(request, 'administrateur/classe_form.html', {'form': form, 'action': 'Ajouter'})

@login_required
@user_passes_test(is_admin)
def classe_modifier(request, pk):
    from etudiant.models import Classe
    from etudiant.forms import ClasseForm
    obj = get_object_or_404(Classe, pk=pk)
    form = ClasseForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        messages.success(request, "Classe modifiée.")
        return redirect('admin_classes')
    return render(request, 'administrateur/classe_form.html', {'form': form, 'action': 'Modifier'})

@login_required
@user_passes_test(is_admin)
def classe_supprimer(request, pk):
    from etudiant.models import Classe
    get_object_or_404(Classe, pk=pk).delete()
    messages.success(request, "Classe supprimée.")
    return redirect('admin_classes')

# ── COMPTES ──
@login_required
@user_passes_test(is_admin)
def comptes(request):
    from etudiant.models import Utilisateur
    return render(request, 'administrateur/comptes.html', {
        'comptes': Utilisateur.objects.all().order_by('-date_joined')
    })

@login_required
@user_passes_test(is_admin)
def compte_activer(request, pk):
    from etudiant.models import Utilisateur
    obj = get_object_or_404(Utilisateur, pk=pk)
    obj.is_active = not obj.is_active
    obj.save()
    messages.success(request, f"Compte {'activé' if obj.is_active else 'désactivé'}.")
    return redirect('admin_comptes')

@login_required
@user_passes_test(is_admin)
def compte_supprimer(request, pk):
    from etudiant.models import Utilisateur
    get_object_or_404(Utilisateur, pk=pk).delete()
    messages.success(request, "Compte supprimé.")
    return redirect('admin_comptes')

# ── ÉTUDIANTS ──
@login_required
@user_passes_test(is_admin)
def etudiants(request):
    from etudiant.models import Etudiant
    return render(request, 'administrateur/etudiants.html', {
        'etudiants': Etudiant.objects.all()
    })
@login_required
@user_passes_test(is_admin)
def profil(request):
    return render(request, 'administrateur/profil.html', {
        'user': request.user
    })


from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # 1. Créer le compte Django standard
            user = form.save()

            # 2. Créer Personne
            from etudiant.models import Personne, Etudiant, Utilisateur

            personne = Personne.objects.create(
                nom=request.POST.get('last_name', ''),
                prenom=request.POST.get('first_name', ''),
            )

            # 3. Créer Utilisateur custom
            utilisateur = Utilisateur.objects.create(
                email=user.email or f"{user.username}@monapp.com",
                password=user.password,
                is_active=True,
            )

            # 4. Créer Etudiant
            from django.db import connection
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO etudiants
                        (personne_ptr_id, utilisateur_id, classe_id)
                    VALUES (%s, %s, NULL)
                    """,
                    [personne.id, utilisateur.id]
                )

            messages.success(request, "Compte créé ! Connectez-vous.")
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})
