from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db import models

import calendar
from datetime import date

from .forms import InscriptionUtilisateurForm, EtudiantForm, RessourceForm, AnnonceForm, ModuleForm
from core.models import Annonce, Ressource, Historique, Etudiant, Enseignant, Notification, Affectation, Module, Classe



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

@login_required
def mon_profil(request):
    return render(request, 'utilisateurs/moncompte.html')

def traitement_global(request):
    if request.method == 'POST':
        enseignant = request.user.profil_enseignant

        if 'btn_ressource' in request.POST:
            form = RessourceForm(request.POST, request.FILES, enseignant=enseignant)
            if form.is_valid():
                ressource = form.save(commit=False)
                ressource.enseignant = enseignant
                ressource.save()

                etudiants = ressource.module.classe.etudiant_set.all()
                for etu in etudiants:
                    Notification.objects.create(
                        titre="Nouvelle ressource",
                        message=ressource.module.intitule,
                        etudiant=etu
                    )
                messages.success(request, "Ressource enregistrée.")

        elif 'btn_annonce' in request.POST:
            form = AnnonceForm(request.POST, enseignant=enseignant)
            if form.is_valid():
                annonce = form.save(commit=False)
                annonce.enseignant = enseignant
                annonce.save()

                etudiants = annonce.classe.etudiant_set.all()
                for etu in etudiants:
                    Notification.objects.create(
                        titre="Nouvelle annonce",
                        message=f"Une nouvelle annonce importante est disponible.",
                        etudiant=etu
                    )
                messages.success(request, "Annonce publiée.")

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
        request.user.profil_etudiant.notifications.filter(
            lue=False,
            titre="Nouvelle annonce"
        ).update(lue=True)
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

    classe = None
    if request.user.is_responsable:
        aff = Affectation.objects.filter(enseignant=request.user.profil_enseignant, est_responsable=True).first()
        if aff:
            classe = aff.classe

    context = {
        'annonces': annonces,
        'cal': cal,
        'semaines': semaines,
        'nom_mois': nom_mois,
        'aujourdhui': aujourdhui.day,
        'classe': classe,
    }
    return render(request, 'utilisateurs/home.html', context)

@login_required
def modules(request):
    if request.user.is_etudiant:
        modules = request.user.profil_etudiant.classe.modules.all() if request.user.profil_etudiant.classe else []
        return render(request, 'utilisateurs/modules.html', {'modules': modules})

    if request.user.is_enseignant:
        enseignant = request.user.profil_enseignant

        modules_gérés = Module.objects.filter(affectations__enseignant=enseignant).distinct()

        classes_responsable = Classe.objects.filter(affectations__enseignant=enseignant, affectations__est_responsable=True)
        modules_responsable = Module.objects.filter(classe__in=classes_responsable).distinct()

        return render(request, 'utilisateurs/modules.html', {
            'modules_gérés': modules_gérés,
            'modules_responsable': modules_responsable
        })

@login_required
def list_ressources(request, module_id):
    module = get_object_or_404(Module, id=module_id)
    ressources = Ressource.objects.filter(module=module).order_by('-date_ajout')

    if hasattr(request.user, 'profil_etudiant'):
        etudiant = request.user.profil_etudiant

        Historique.objects.create(etudiant=etudiant, action='consultation')

        etudiant.notifications.filter(
            lue=False,
            titre="Nouvelle ressource",
            message__contains=module.intitule
        ).update(lue=True)

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

@login_required
def historique_etudiants(request):
    ens = request.user.profil_enseignant

    aff_resp = Affectation.objects.filter(enseignant=ens, est_responsable=True).first()
    classe = aff_resp.classe if aff_resp else None

    modules_intervenant = Affectation.objects.filter(enseignant=ens).values_list('module', flat=True)

    query = models.Q(ressource__module__in=modules_intervenant)

    if request.user.is_responsable:
        classes_resp = Affectation.objects.filter(enseignant=ens, est_responsable=True).values_list('classe', flat=True)
        query |= models.Q(etudiant__classe__in=classes_resp)

    historiques = Historique.objects.filter(query).distinct().order_by('-date_datetime')

    return render(request, 'utilisateurs/professeur/historique.html', {
        'historiques': historiques,
        'classe': classe
    })

@login_required
def gestion_classe(request, classe_id):
    classe = get_object_or_404(Classe, pk=classe_id)
    if not Affectation.objects.filter(enseignant=request.user.profil_enseignant, classe=classe, est_responsable=True).exists():
        return redirect('utilisateurs:home')

    if request.method == 'POST':

        if 'ajouter_module' in request.POST:
            ens_id = request.POST.get('enseignant_id')
            mod_id = request.POST.get('module_id')
            ens = Enseignant.objects.get(pk=ens_id)
            mod = Module.objects.get(pk=mod_id)

            aff_admin = Affectation.objects.filter(enseignant=ens, classe=classe, module__isnull=True).first()

            if aff_admin:
                aff_admin.module = mod
                aff_admin.save()
            else:
                Affectation.objects.create(enseignant=ens, classe=classe, module=mod, date_debut=timezone.now())

        elif 'retirer_module' in request.POST:
            Affectation.objects.filter(pk=request.POST.get('aff_id')).delete()

        if 'ajouter' in request.POST:
            etudiant_id = request.POST.get('etudiant_id')
            etudiant = Etudiant.objects.get(pk=etudiant_id)
            etudiant.classe = classe
            etudiant.save()
            messages.success(request, "Étudiant ajouté à la classe.")

        elif 'retirer' in request.POST:
            etudiant_id = request.POST.get('etudiant_id')
            etudiant = Etudiant.objects.get(pk=etudiant_id)
            etudiant.classe = None
            etudiant.save()
            messages.success(request, "Étudiant retiré de la classe.")

        if 'ajouter_module_classe' in request.POST:
            form = ModuleForm(request.POST)
            if form.is_valid():
                nouveau_module = form.save(commit=False)
                nouveau_module.classe = classe
                nouveau_module.save()
        elif 'supprimer_module' in request.POST:
            module_id = request.POST.get('module_id')
            Module.objects.filter(pk=module_id, classe=classe).delete()
        elif 'modifier_module' in request.POST:
            module_id = request.POST.get('module_id')
            module_instance = get_object_or_404(Module, pk=module_id, classe=classe)
            form = ModuleForm(request.POST, instance=module_instance)
            if form.is_valid():
                form.save()

    context = {
        'classe': classe,
        'profs_de_classe': Enseignant.objects.filter(affectations__classe=classe).distinct(),
        'tous_modules': Module.objects.filter(classe=classe).exclude(
            affectations__classe=classe,
            affectations__module__isnull=False
        ),
        'modules_classe': Module.objects.filter(classe=classe),
        'etudiants_dans_classe': Etudiant.objects.filter(classe=classe),
        'etudiants_sans_classe': Etudiant.objects.filter(classe__isnull=True),
        'tous_enseignants': Enseignant.objects.all()
    }
    return render(request, 'utilisateurs/professeur/classe.html', context)
