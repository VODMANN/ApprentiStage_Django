from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UtilisateurForm, EtudiantForm, EnseignantForm, SecretaireForm,SoutenanceForm
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.views import LoginView
from .models import ProfilEtudiant, Entreprise, Contrat,Soutenance,Salle,Utilisateur,ProfilEnseignant
from django.contrib.auth.views import redirect_to_login

from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from datetime import datetime, timedelta  
from icalendar import Calendar, Event


def user_type_required(user_type):
    def decorator(view_func):
        @login_required
        def _wrapped_view(request, *args, **kwargs):
            user = request.user
            if user.is_authenticated:
                try:
                    # Accéder au profil associé au type d'utilisateur
                    profile = getattr(user, f'profil{user_type.lower()}')
                except AttributeError:
                    return HttpResponseForbidden('Vous n\'avez pas les droits nécessaires pour accéder à cette page.')
            else:
                return redirect_to_login(request.get_full_path())

            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator


class UserLoginView(LoginView):
    template_name = 'registration/login.html'

def home(request):
  if request.user.is_authenticated:
        user_type = request.user.type_utilisateur
        print(user_type)
  return render(request, 'pages/accueil.html')

# @login_required
# @user_type_required('secretaire')
def signup(request):
    print('//////////////////////////////')
    if request.method == 'POST':
        user_form = UtilisateurForm(request.POST)
        etudiant_form = EtudiantForm(request.POST)
        enseignant_form = EnseignantForm(request.POST)
        secretaire_form = SecretaireForm(request.POST)

        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user_type = user_form.cleaned_data['type_utilisateur']  # Assurez-vous que cela correspond au nom dans votre modèle

            if user_type == 'etudiant' and etudiant_form.is_valid():
                user.save()
                etudiant = etudiant_form.save(commit=False)
                etudiant.utilisateur = user
                etudiant.save()
                return redirect('lesApprentiStage:home')
            elif user_type == 'enseignant' and enseignant_form.is_valid():
                user.save()
                enseignant = enseignant_form.save(commit=False)
                enseignant.utilisateur = user
                enseignant.save()
                # Log in the user here if needed
                return redirect('lesApprentiStage:home')
            elif user_type == 'secretaire' and secretaire_form.is_valid():
                user.save()
                secretaire = secretaire_form.save(commit=False)
                secretaire.utilisateur = user
                secretaire.save()
                # Log in the user here if needed
                return redirect('lesApprentiStage:home')

    else:
        user_form = UtilisateurForm()
        etudiant_form = EtudiantForm()
        enseignant_form = EnseignantForm()
        secretaire_form = SecretaireForm()

    return render(request, 'registration/signup.html', {
        'user_form': user_form,
        'etudiant_form': etudiant_form,
        'enseignant_form': enseignant_form,
        'secretaire_form': secretaire_form,
    })

@login_required
@user_type_required('secretaire')
def pageRecherche(request):
    return render(request, 'pages/recherche.html')


@login_required
@user_type_required('secretaire')
def search(request):
    query = request.GET.get('query', '')
    search_type = request.GET.get('type', '')

    if search_type == 'ETUDIANT':
        results = ProfilEtudiant.objects.filter(nomEtu__icontains=query).values('numEtu','civiliteEtu','nomEtu','prenomEtu','adresseEtu','cpEtu','villeEtu','telEtu','promo')
    elif search_type == 'ENTREPRISE':
        results = Entreprise.objects.filter(nomEnt__icontains=query)
    elif search_type == 'CONTRAT':
        results = Contrat.objects.filter(type__icontains=query)
    else:
        results = []

    if request.headers.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        return render(request, 'results.html', {"results": results})

    return render(request, 'pages/recherche.html', {"results": results, "search_type": search_type})

@login_required
def soutenance(request):
    user_type_to_view_func = {
        'secretaire': soutenance_sec,
        'etudiant': soutenance_etu,
        'enseignant': soutenance_ens,
    }
    
    user_type = request.user.type_utilisateur
    view_func = user_type_to_view_func.get(user_type)
    
    if view_func:
        return view_func(request, user_type)
    else:
        return HttpResponseForbidden("Type d'utilisateur non autorisé pour cette action.")


@login_required
def soutenance_sec(request, user_type):
    if request.method == 'POST':
        formSoutenance = SoutenanceForm(request.POST)
        if formSoutenance.is_valid():
            salle = formSoutenance.cleaned_data['salle']
            heureSoutenance = formSoutenance.cleaned_data['heureSoutenance']
            dateSoutenance = formSoutenance.cleaned_data['dateSoutenance']
            verification = Soutenance.objects.filter(
                salle=salle, 
                heureSoutenance=heureSoutenance,
                dateSoutenance=dateSoutenance
            )
            if not verification.exists():
                formSoutenance.save()
                messages.success(request, "La soutenance a été ajoutée avec succès.")
                return redirect('lesApprentiStage:soutenance')
            else:
                messages.error(request, "Une soutenance est déjà programmée dans cette salle à cette heure et date.")
        else:
            messages.error(request, "Il y a eu un problème avec le formulaire.")
    else:
        formSoutenance = SoutenanceForm()
    listSoutenance = Soutenance.objects.all()
    return render(request, 'pages/soutenance.html', {
        "form": formSoutenance,
        'listSoutenance': listSoutenance, 
        'user': user_type
    })

@login_required
def soutenance_etu(request, user_type):
    unUtilisateur = get_object_or_404(Utilisateur, username=request.user.username)
    unEtudiant = get_object_or_404(ProfilEtudiant, utilisateur=unUtilisateur)
    lesContrats = Contrat.objects.filter(etudiant=unEtudiant)  # Récupérer tous les contrats pour l'étudiant
    etuSoutenances = Soutenance.objects.filter(idContrat__in=lesContrats)  # Utiliser '__in' pour filtrer par les contrats récupérés
    return render(request, 'pages/soutenance.html', {
        'etuSoutenances': etuSoutenances,  # Passer les soutenances en contexte
        'user': user_type
    })


@login_required
def soutenance_ens(request, user_type):
    unUtilisateur = get_object_or_404(Utilisateur, username=request.user.username)
    unEnseignant = get_object_or_404(ProfilEnseignant, utilisateur=unUtilisateur)
    unContrat = Contrat.objects.filter(enseignant=unEnseignant)
    enSoutenance = Soutenance.objects.filter(idContrat__in=unContrat) | Soutenance.objects.filter(candide=unEnseignant)
    listCandideSoutenance = Soutenance.objects.filter(candide=None).exclude(idContrat__in=unContrat)
    return render(request, 'pages/soutenance.html', {
        'enSoutenance': enSoutenance,
        'user': user_type, 
        'listCandideSoutenance': listCandideSoutenance, 
        'enseignant': unEnseignant
    })








@login_required
def supprimerSoutenance(request,id):
    unesoutenance = Soutenance.objects.filter(id = id)[0]
    unesoutenance.delete()
    return redirect('lesApprentiStage:soutenance')

@login_required
def modifierSoutenance(request, id):
    unesoutenance = get_object_or_404(Soutenance, id=id)
    listSoutenance = Soutenance.objects.all()
    if request.method == 'POST':
        formSoutenance = SoutenanceForm(request.POST, instance=unesoutenance)
        if formSoutenance.is_valid():
            salle = formSoutenance.cleaned_data['salle']
            heureSoutenance = formSoutenance.cleaned_data['heureSoutenance']
            dateSoutenance = formSoutenance.cleaned_data['dateSoutenance']
            verification = Soutenance.objects.filter(
                salle=salle, 
                heureSoutenance=heureSoutenance, 
                dateSoutenance=dateSoutenance
            ).exclude(id=id)
            if not verification.exists():
                formSoutenance.save()
                messages.success(request, "La soutenance a été modifiée avec succès.")
                return redirect('lesApprentiStage:soutenance')
            else:
                messages.error(request, "Impossible de modifier la soutenance car la salle est déjà réservée à cet horaire.")
        else:
            messages.error(request, "Il y a eu un problème avec le formulaire.")
    else:
        formSoutenance = SoutenanceForm(instance=unesoutenance)
    return render(request, 'pages/soutenance.html', {
        "form": formSoutenance, 
        'modifSoutenance': unesoutenance, 
        'listSoutenance': listSoutenance,
        'user': request.user.type_utilisateur
    })

@login_required
def inscrireSoutenance(request,id):
    unUtilisateur = Utilisateur.objects.filter(username = request.user.username)[0]
    unEnseignant = ProfilEnseignant.objects.filter(utilisateur = unUtilisateur)[0]
    unesoutenance = Soutenance.objects.filter(id = id)[0]
    unesoutenance.candide = unEnseignant
    unesoutenance.save()
    return redirect('lesApprentiStage:soutenance')


@login_required
def desinscrireSoutenance(request,id):
    unesoutenance = Soutenance.objects.filter(id = id)[0]
    unesoutenance.candide = None
    unesoutenance.save()
    return redirect('lesApprentiStage:soutenance')




@login_required
def calendar_events(request):
    events = []

    # Assurez-vous que seul un enseignant peut accéder à cette vue
    if request.user.type_utilisateur != 'enseignant':
        return JsonResponse({'error': 'Unauthorized'}, status=403)

    # Obtenez le profil enseignant connecté
    profil_enseignant = get_object_or_404(ProfilEnseignant, utilisateur=request.user)

    # Filtrez les soutenances où l'utilisateur est le candide
    soutenances = Soutenance.objects.filter(candide=profil_enseignant)

    for soutenance in soutenances:
        event = {
            'title': f'Soutenance: {soutenance.idContrat.etudiant.nomEtu} {soutenance.idContrat.etudiant.prenomEtu}',
            'start': f'{soutenance.dateSoutenance.isoformat()}T{soutenance.heureSoutenance.isoformat()}',
            'end': (datetime.combine(soutenance.dateSoutenance, soutenance.heureSoutenance) + timedelta(hours=1)).isoformat(),
            'url': '',  # URL pour accéder aux détails de la soutenance si nécessaire
            'allDay': False
        }
        
        events.append(event)

    return JsonResponse(events, safe=False)


def export_calendar(request):
    # Créer un calendrier
    cal = Calendar()

    # Récupérer les événements depuis la base de données
    events = Soutenance.objects.filter(candide=request.user.profilenseignant)

    for soutenance in events:
        event = Event()
        event.add('summary', 'Soutenance ' + soutenance.idContrat.etudiant.nomEtu)
        event.add('dtstart', datetime.combine(soutenance.dateSoutenance, soutenance.heureSoutenance))
        event.add('dtend', datetime.combine(soutenance.dateSoutenance, soutenance.heureSoutenance) + timedelta(hours=1))
        event.add('dtstamp', datetime.now())
        # Ajouter d'autres propriétés si nécessaire...
        
        cal.add_component(event)

    response = HttpResponse(cal.to_ical(), content_type="text/calendar")
    response['Content-Disposition'] = 'attachment; filename="soutenances.ics"'
    return response

def calendar_ens(request):
    return render(request, 'pages/calendrier_ens.html')