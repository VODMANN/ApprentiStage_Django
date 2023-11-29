from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required

from .forms import ContratEtudiantForm, EntrepriseForm, EtudiantProfilForm, ResponsableForm, ThemeForm, TuteurForm, UtilisateurForm, EtudiantForm, EnseignantForm, SecretaireForm, SoutenanceForm
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import redirect_to_login

from .models import Departement, Document, EnseignantPromo, Evaluation, Offre, ProfilEtudiant, Entreprise, Contrat, Promo, Theme, Utilisateur,Soutenance,Salle,ProfilEnseignant
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from datetime import datetime, timedelta, timezone  
from icalendar import Calendar, Event
import csv
from django.contrib.auth.hashers import make_password


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
    offre_list = Offre.objects.all()   
    user = request.user

    if request.user.is_authenticated:
        user_type = request.user.type_utilisateur
        print(user_type)
        if user_type == 'etudiant':
          return render(request, 'etudiant/accueil_etu.html', {'offre_list': offre_list})
        if user_type == 'enseignant':
            is_responsible = user.profilenseignant.roleEnseignant in ['chef_departement', 'enseignant_promo']
            return render(request, 'enseignant/accueil_ens.html',{'user': user, 'is_responsible': is_responsible})
    return render(request, 'pages/accueil.html')

""" @login_required
@user_type_required('secretaire') """
def signup(request):
    promos = Promo.objects.all()  
    if request.method == 'POST':
        user_form = UtilisateurForm(request.POST)
        etudiant_form = EtudiantForm(request.POST)
        enseignant_form = EnseignantForm(request.POST)
        secretaire_form = SecretaireForm(request.POST)

        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user_type = user_form.cleaned_data['type_utilisateur']  

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

                if enseignant.roleEnseignant == ProfilEnseignant.CHEF_DEPARTEMENT:
                    selected_departement = enseignant_form.cleaned_data.get('departements')
                    if selected_departement:
                        selected_departement.chef = enseignant
                        selected_departement.save()

                selected_promos = enseignant_form.cleaned_data.get('promos')
                for promo in selected_promos:
                    EnseignantPromo.objects.create(enseignant=enseignant, promo=promo)
                return redirect('lesApprentiStage:home')
            
            elif user_type == 'secretaire' and secretaire_form.is_valid():
                user.save()
                secretaire = secretaire_form.save(commit=False)
                secretaire.utilisateur = user
                secretaire.save()
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
        'promos': promos,
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
    promo_filter = request.GET.get('promo', '')  # Récupère la valeur de la promotion depuis la requête GET

    search_mapping = {
        'ETUDIANT': (ProfilEtudiant, ['civiliteEtu','nomEtu', 'prenomEtu', 'numEtu', 'adresseEtu', 'cpEtu', 'villeEtu', 'telEtu', 'promo', 'idDepartement__nomDep']),
        'ENTREPRISE': (Entreprise, ['nomEnt', 'numSiret', 'adresseEnt', 'cpEnt', 'villeEnt', 'responsable__nomResp', 'responsable__prenomResp', 'responsable__emailResp']),
        'CONTRAT': (Contrat, ['type', 'description', 'etat', 'dateDeb', 'dateFin', 'etudiant__civiliteEtu', 'etudiant__nomEtu', 'etudiant__prenomEtu', 'etudiant__numEtu', 'entreprise__nomEnt', 'entreprise__adresseEnt', 'entreprise__cpEnt', 'entreprise__villeEnt']),
    }

    results = []
    if search_type in search_mapping:
        model, fields = search_mapping[search_type]
        query_objects = Q()
        for field in fields:
            query_objects |= Q(**{f'{field}__icontains': query})

        if promo_filter:  # Vérifie si un filtre de promotion est appliqué
            query_objects &= Q(promo__icontains=promo_filter)

        results = model.objects.filter(query_objects).values(*fields)

    if request.headers.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        data = list(results)
        return JsonResponse(data, safe=False)

    return render(request, 'pages/recherche.html', {"results": results, "search_type": search_type})

@login_required
def soutenance(request):
    print(request.user.type_utilisateur)
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
@user_type_required('etudiant')
def ajouter_contrat(request):
    if request.method == 'POST':
        form = ContratEtudiantForm(request.POST)
        if form.is_valid():
            contrat = form.save(commit=False)
            try:
                profil_etudiant = request.user.profiletudiant
            except Utilisateur.profiletudiant.RelatedObjectDoesNotExist:
                messages.error(request, "Vous devez avoir un profil étudiant pour ajouter un contrat.")
                return redirect('lesApprentiStage:home')

            contrat.etudiant = profil_etudiant
            contrat.save()
            messages.success(request, "Contrat ajouté avec succès.")
            return redirect('lesApprentiStage:ajouter_responsable', contrat_id=contrat.id)
        
    else:
        form = ContratEtudiantForm()
    
    return render(request, 'etudiant/ajouter_contrat.html', {'form': form, 'EntrepriseForm': EntrepriseForm(), 'ThemeForm': ThemeForm()})


@login_required
def ajouter_entrepriseSeul(request):
    if request.method == 'POST':
        form = EntrepriseForm(request.POST)
        if form.is_valid():
            entreprise = form.save()
            messages.success(request, "Entreprise ajoutée avec succès.")
            return redirect('lesApprentiStage:home') 
        else:
            return JsonResponse({"success": False, "errors": form.errors}, status=400)
    else:
        form = EntrepriseForm()

    return render(request, 'pages/ajouter_entreprise.html', {'EntrepriseForm': form})


@login_required
def ajouter_entreprise(request):
    if request.method == 'POST':
        form = EntrepriseForm(request.POST)
        if form.is_valid():
            entreprise = form.save()
            messages.success(request, "Entreprise ajoutée avec succès.")
            return JsonResponse({"success": True, "entreprise": {"nomEnt": entreprise.nomEnt, "pk": entreprise.pk}})
        else:
            return JsonResponse({"success": False, "errors": form.errors})
    else:
        form = EntrepriseForm()

    return render(request, 'pages/ajouter_entreprise.html', {'EntrepriseForm': form})



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
            'url': '',
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

def ajouter_theme(request):
    if request.method == 'POST':
        form = ThemeForm(request.POST)
        if form.is_valid():
            theme = form.save()
            messages.success(request, "Thème ajouté avec succès.")
            return JsonResponse({"success": True, "theme": {"nomTheme": theme.nomTheme, "pk": theme.pk}})
        else:
            return JsonResponse({"success": False, "errors": form.errors})
    else:
        form = ThemeForm()

    return render(request, 'pages/ajouter_theme.html', {'ThemeForm': form})


def ajouter_responsable(request, contrat_id):
    contrat = get_object_or_404(Contrat, pk=contrat_id)
    entreprise = contrat.entreprise

    if request.method == 'POST':
        responsable_form = ResponsableForm(request.POST, entreprise=entreprise)
        tuteur_form = TuteurForm(request.POST)
        if responsable_form.is_valid() and tuteur_form.is_valid():
            responsable = responsable_form.save(commit=False)
            tuteur = tuteur_form.save(commit=False)
            if responsable_form.cleaned_data['responsable_existant']:
                responsable = responsable_form.cleaned_data['responsable_existant']
            else:
                responsable.entreprise = entreprise
                responsable.save()
            tuteur.entreprise = entreprise
            tuteur.save()
            contrat.responsable = responsable
            contrat.tuteur = tuteur
            contrat.save()
            messages.success(request, "Responsable et tuteur ajoutés avec succès.")
            return redirect('lesApprentiStage:home')
    else:
        responsable_form = ResponsableForm(entreprise=entreprise)
        tuteur_form = TuteurForm()

    context = {
        'responsable_form': responsable_form,
        'tuteur_form': tuteur_form
    }
    return render(request, 'pages/ajouter_responsable.html', context)

@login_required
@user_type_required('secretaire')
def details_etudiant(request, etudiant_id):
    etudiant = get_object_or_404(ProfilEtudiant, numEtu=etudiant_id)
    contrats_stage = Contrat.objects.filter(etudiant=etudiant, type='stage')
    contrats_apprentissage = Contrat.objects.filter(etudiant=etudiant, type='apprentissage')

    context = {
        'etudiant': etudiant,
        'contrats_stage': contrats_stage,
        'contrats_apprentissage': contrats_apprentissage,
    }
    return render(request, 'admin/detailsEtu.html', context)

@login_required
@user_type_required('secretaire')
def details_entreprise(request, entreprise_id):
    entreprise = get_object_or_404(Entreprise, numSiret=entreprise_id)

    context = {
        'entreprise': entreprise,
    }
    return render(request, 'admin/detailsEnt.html', context)

def affichage_contrat(request, contrat_id):
    contrat = get_object_or_404(Contrat, id=contrat_id)

    # Assurez-vous que la relation avec l'entreprise existe
    if contrat.entreprise:
        # Utilisez la relation inverse à partir du modèle Responsable
        responsable_entreprise = contrat.entreprise.responsable_set.first()
    else:
        responsable_entreprise = None

    context = {
        'contrat': contrat,
        'entreprise': contrat.entreprise,
        'tuteur': contrat.tuteur,
        'responsable_entreprise': responsable_entreprise,
    }

    return render(request, 'admin/affichageContrat.html', context)



def offre_detail(request, offre_id):
    offre = Offre.objects.get(pk=offre_id)
    return render(request, 'etudiant/offre_detail.html', {'offre': offre})

def recherche_offres(request):
    theme = Theme.objects.all()
    entreprise = Entreprise.objects.all()

    query = request.GET.get('query', '')
    entreprise_id = request.GET.get('entreprise', '')
    theme_id = request.GET.get('theme', '')
    date_min = request.GET.get('date_min', '')
    date_max = request.GET.get('date_max', '')

    queryset = Offre.objects.all()
    if entreprise_id:
        queryset = queryset.filter(entreprise__id=entreprise_id)
    if theme_id:
        queryset = queryset.filter(theme__id=theme_id)
    if date_min:
        queryset = queryset.filter(datePublication__gte=date_min)
    if date_max:
        queryset = queryset.filter(datePublication__lte=date_max)

    # Recherche sur plusieurs champs en utilisant Q objects
    if query:
        queryset = queryset.filter(
            Q(titre__icontains=query) |
            Q(description__icontains=query) |
            Q(competences__icontains=query)
        )
    # Renommez 'results' en 'queryset' pour être cohérent avec le filtrage ci-dessus
    return render(request, 'etudiant/recherche_offres.html', {'results': queryset, 'theme': theme, 'entreprise': entreprise})


@login_required
def edit_etudiant(request):
    if request.user.type_utilisateur != 'etudiant':
        # Rediriger l'utilisateur ou afficher une erreur car il n'est pas un étudiant
        return redirect('page_d_erreur')

    profil_etudiant, created = ProfilEtudiant.objects.get_or_create(utilisateur=request.user)

    if request.method == 'POST':
        form = EtudiantForm(request.POST, instance=profil_etudiant)
        if form.is_valid():
            form.save()
            # Ajouter un message de succès
            messages.success(request, "Votre profil a été mis à jour avec succès.")
            # Rediriger l'utilisateur vers une autre page, comme le tableau de bord
            return redirect('lesApprentiStage:home')
    else:
        form = EtudiantProfilForm(instance=profil_etudiant)

    return render(request, 'etudiant/edit_etudiant.html', {'form': form})


@login_required
def profile(request):
    etudiant = request.user.profiletudiant
    contrats = Contrat.objects.filter(etudiant=etudiant).select_related('entreprise', 'theme', 'tuteur', 'enseignant')
    documents = Document.objects.filter(contrat__etudiant=etudiant)
    evaluations = Evaluation.objects.filter(contrat__etudiant=etudiant)
    soutenance = Soutenance.objects.filter(idContrat__etudiant=request.user.profiletudiant)
    print(soutenance)
    # Vous pouvez ajouter d'autres éléments si besoin

    context = {
        'etudiant': etudiant,
        'contrats': contrats,
        'documents': documents,
        'evaluations': evaluations,
        'soutenances': soutenance,
    }
    return render(request, 'etudiant/profile.html', context)



def upload_csv(request):
    if request.method == "GET":
        return render(request, 'secretariat/upload_csv.html')

    csv_file = request.FILES['file']
    if not csv_file.name.endswith('.csv'):
        return HttpResponse("Le fichier n'est pas un CSV")

    file_data = csv_file.read().decode("utf-8")
    lines = file_data.split("\n")

    for line in lines:
        fields = line.split(",")
        if fields and len(fields) > 1:
            departement_id = fields[10]

            try:
                departement = Departement.objects.get(id=departement_id)
            except Departement.DoesNotExist:
                return HttpResponse(f"Erreur : le département avec l'ID {departement_id} n'existe pas", status=400)

            username = fields[1] + '_' + fields[2]
            password = make_password('password_par_defaut')
            user, created = Utilisateur.objects.get_or_create(username=username, defaults={'password': password, 'type_utilisateur': 'etudiant'})
            
            ProfilEtudiant.objects.update_or_create(
                utilisateur=user,
                nomEtu=fields[1],
                prenomEtu=fields[2],
                numEtu=fields[3],
                civiliteEtu=fields[4],
                adresseEtu=fields[5],
                cpEtu=fields[6],
                villeEtu=fields[7],
                telEtu=fields[8],
                promo=fields[9],
                idDepartement=departement,
            )

    return redirect('lesApprentiStage:home')

def suivi_etudiants(request):
    user = request.user
    enseignant = ProfilEnseignant.objects.get(utilisateur=user)
    
    if enseignant.roleEnseignant == ProfilEnseignant.CHEF_DEPARTEMENT:
        etudiants = ProfilEtudiant.objects.filter(idDepartement__chef=enseignant)
    elif enseignant.roleEnseignant == ProfilEnseignant.ENSEIGNANT_PROMO:
        promos_gerees = EnseignantPromo.objects.filter(enseignant=enseignant).values_list('promo', flat=True)
        etudiants = ProfilEtudiant.objects.filter(promo__in=promos_gerees)
    else:
        etudiants = ProfilEtudiant.objects.none()

    filter_stage = request.GET.get('stage', None)
    if filter_stage == 'sans_stage':
        etudiants = etudiants.exclude(
            contrat__estValide=True,
        )
    return render(request, 'enseignant/suivi_etudiants.html', {'etudiants': etudiants})
