from .forms import RessourceForm, AnnonceForm
from core.models import Notification, Classe, Module

def modal_forms(request):
    if request.user.is_authenticated and request.user.is_enseignant:
        enseignant_profile = getattr(request.user, 'profil_enseignant', None)
        if enseignant_profile:
            return {
                'ressource_form': RessourceForm(enseignant=enseignant_profile),
                'annonce_form': AnnonceForm(enseignant=enseignant_profile)
            }
    return {'ressource_form': None, 'annonce_form': None}

def modules_process(request):
    if request.user.is_authenticated:
        if request.user.is_etudiant:
            profil_etudiant = getattr(request.user, 'profil_etudiant', None)
            modules = profil_etudiant.classe.modules.all() if (profil_etudiant and profil_etudiant.classe) else []
            return {'modules': modules}

        if request.user.is_enseignant:
            enseignant = getattr(request.user, 'profil_enseignant', None)
            if enseignant:
                modules_gérés = Module.objects.filter(affectations__enseignant=enseignant).distinct()
                classes_responsable = Classe.objects.filter(affectations__enseignant=enseignant, affectations__est_responsable=True)
                modules_responsable = Module.objects.filter(classe__in=classes_responsable).distinct()
                return {
                    'modules_gérés': modules_gérés,
                    'modules_responsable': modules_responsable
                }
    return {}

def classes_responsables_processor(request):
    if request.user.is_authenticated and request.user.is_enseignant:
        enseignant = getattr(request.user, 'profil_enseignant', None)
        if enseignant:
            classes = Classe.objects.filter(
                affectations__enseignant=enseignant,
                affectations__est_responsable=True
            ).distinct()
            return {'classes_responsables': classes}
    return {'classes_responsables': []}

def notifications_processor(request):
    if request.user.is_authenticated and request.user.is_etudiant:
        # On vérifie d'abord si le profil étudiant existe
        profil_etudiant = getattr(request.user, 'profil_etudiant', None)
        if profil_etudiant:
            notifs = Notification.objects.filter(
                etudiant=profil_etudiant,
                lue=False
            ).order_by('-date_datetime')
            return {
                'notifications': notifs,
                'nombre_notifs': notifs.count()
            }
    return {'notifications': [], 'nombre_notifs': 0}
