import calendar
from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import InscriptionUtilisateurForm, EtudiantForm, RessourceForm, AnnonceForm
from django.contrib.auth.decorators import login_required
from .models import Annonce, Ressource, Historique
from administrateur.models import Affectation, Module

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
            return redirect('authentification:connexion')
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

def traitement_global(request):
    if request.method == 'POST':
        if 'btn_ressource' in request.POST:
            enseignant_profile = request.user.profil_enseignant
            form = RessourceForm(request.POST, request.FILES, enseignant=enseignant_profile)

            if form.is_valid():
                ressource = form.save(commit=False)
                ressource.enseignant = enseignant_profile
                ressource.save()

                messages.success(request, "Ressource enregistrée.")
        if 'btn_annonce' in request.POST:
            form = AnnonceForm(request.POST, enseignant=request.user.profil_enseignant)
            if form.is_valid():
                annonce = form.save(commit=False)
                annonce.enseignant = request.user.profil_enseignant
                annonce.save()

    return redirect(request.META.get('HTTP_REFERER', 'utilisateurs:home'))

@login_required
def home(request):
    annonces = Annonce.objects.none()
    aujourdhui = date.today()
    cal = calendar.monthcalendar(aujourdhui.year, aujourdhui.month)
    nom_mois = aujourdhui.strftime("%B")

    semaines = []
    for semaine in cal:
        semaines.append({
            'jours': semaine,
            'evenements': []
        })

    if request.user.is_etudiant:
        if hasattr(request.user, 'profil_etudiant') and request.user.profil_etudiant.classe:
            annonces = Annonce.objects.filter(
                classe=request.user.profil_etudiant.classe
            ).order_by('-date_datetime')

    elif request.user.is_enseignant:
        classes_enseignees = Affectation.objects.filter(
            enseignant=request.user.profil_enseignant
        ).values_list('classe', flat=True)

        annonces = Annonce.objects.filter(
            classe__in=classes_enseignees
        ).select_related('classe', 'enseignant').order_by('-date_datetime')

    context = {
        'annonces': annonces,
        'cal': cal,
        'semaines': semaines,
        'nom_mois': nom_mois,
        'aujourdhui': aujourdhui.day,
    }
    return render(request, 'utilisateurs/home.html', context)

@login_required
def modules(request):
    modules = None

    if request.user.is_enseignant:
        modules = Module.objects.filter(affectations__enseignant=request.user.profil_enseignant).distinct()

    elif request.user.is_etudiant:
        if request.user.profil_etudiant.classe:
            modules = request.user.profil_etudiant.classe.modules.all()
        else:
            modules = []

    return render(request, 'utilisateurs/modules.html', {'modules': modules})

@login_required
def list_ressources(request, module_id):
    module = get_object_or_404(Module, id=module_id)
    ressources = Ressource.objects.filter(module=module).order_by('-date_ajout')

    if hasattr(request.user, 'profil_etudiant'):
        etudiant = request.user.profil_etudiant
        Historique.objects.create(
            etudiant=etudiant,
            action='consultation'
        )

    context = {
        'module': module,
        'ressources': ressources,
    }
    return render(request, 'utilisateurs/ressources.html', context)

@login_required
def telecharger_ressource(request, ressource_id):
    ressource = get_object_or_404(Ressource, id=ressource_id)

    if hasattr(request.user, 'profil_etudiant'):
        Historique.objects.create(
            etudiant=request.user.profil_etudiant,
            action='telechargement',
            ressource=ressource
        )

    return redirect(ressource.fichier.url)
