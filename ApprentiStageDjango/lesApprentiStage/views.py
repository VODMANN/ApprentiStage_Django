from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required

from .utils import generer_convention

from .forms import *
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseNotAllowed, JsonResponse
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import redirect_to_login

from .models import *
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
from datetime import date
from django.contrib.auth.models import User
from django.utils import timezone

def insertion(request):
    # Création des instances Utilisateur (Utilisateur personnalisé)
    etudiant = Utilisateur.objects.create_user(
        username='etudiant123',
        email='etudiant@example.com',
        password='etudiantpassword',
        first_name='John',
        last_name='Doe',
        type_utilisateur='etudiant'  # Ajoutez le champ type_utilisateur selon votre modèle
    )

    enseignant = Utilisateur.objects.create_user(
        username='enseignant456',
        email='enseignant@example.com',
        password='enseignantpassword',
        first_name='Alice',
        last_name='Smith',
        type_utilisateur='enseignant'  # Ajoutez le champ type_utilisateur selon votre modèle
    )

    secretaire = Utilisateur.objects.create_user(
        username='secretaire789',
        email='secretaire@example.com',
        password='secretairepassword',
        first_name='Bob',
        last_name='Johnson',
        type_utilisateur='secretaire'  # Ajoutez le champ type_utilisateur selon votre modèle
    )
    
    profil_enseignant = ProfilEnseignant.objects.create(
        utilisateur=enseignant,
        numHarpege='123ABC',
        nomEnseignant='Smith',
        prenomEnseignant='Alice',
        mailEnseignant='enseignant@example.com',
        roleEnseignant='chef_departement'
    )
    
    # Création des instances Departement, Entreprise, Theme
    departement_info = Departement.objects.create(
        nomDep='Département Informatique',
        adresseDep='123 Rue des Développeurs',
        chef=profil_enseignant  # Vous pouvez attribuer un enseignant existant comme chef de département
    )
    
    # Création des instances Promo
    promo_info = Promo.objects.create(
        nomPromo='1B',
        annee=2023,
        departement=departement_info
    )
    
    # Création des instances ProfilEtudiant, ProfilEnseignant, ProfilSecretaire
    profil_etudiant = ProfilEtudiant.objects.create(
        utilisateur=etudiant,
        nomEtu='Doe',
        prenomEtu='John',
        numEtu='E12345',
        civiliteEtu='M.',
        adresseEtu='789 Avenue des Étudiants',
        cpEtu=54321,
        villeEtu='Ville Étudiant',
        telEtu='0123456789',
        promo=promo_info,
        idDepartement=departement_info
    )



    profil_secretaire = ProfilSecretaire.objects.create(
        utilisateur=secretaire,
        numSec='S123'
    )




    entreprise_info = Entreprise.objects.create(
        numSiret='123456789',
        nomEnt='Entreprise XYZ',
        adresseEnt='456 Rue des Entreprises',
        cpEnt=12345,
        villeEnt='Ville Entreprise'
    )

    theme_info = Theme.objects.create(
        nomTheme='Développement Web'
    )



    
    
        # Création des instances EnseignantPromo
    enseignant_promo = EnseignantPromo.objects.create(
        enseignant=profil_enseignant,
        promo=promo_info
    )

    # Création des instances Responsable, Tuteur, Contrat
    responsable_entreprise = Responsable.objects.create(
        nomResp='Nom Responsable',
        prenomResp='Prénom Responsable',
        emailResp='responsable@entreprise.com',
        entreprise=entreprise_info
    )

    tuteur_entreprise = Tuteur.objects.create(
        nomTuteur='Nom Tuteur',
        prenomTuteur='Prénom Tuteur',
        metierTuteur='Métier Tuteur',
        telTuteur='9876543210',
        emailTuteur='tuteur@entreprise.com',
        entreprise=entreprise_info
    )

    contrat_info = Contrat.objects.create(
        type='Type Contrat',
        description='Description Contrat',
        etat='État Contrat',
        gratification='Gratification Contrat',
        dateDeb=timezone.now(),
        dateFin=timezone.now() + timezone.timedelta(days=90),  # Exemple : Contrat pour 90 jours
        estValide=True,
        etudiant=profil_etudiant,
        enseignant=profil_enseignant,
        tuteur=tuteur_entreprise,
        theme=theme_info,
        entreprise=entreprise_info,
        enFrance=True
    )


    
    # Création des instances Offre, Salle, Soutenance, Document, Evaluation
    offre_info = Offre.objects.create(
        titre='Titre Offre',
        description='Description Offre',
        mailRh='rh@entreprise.com',
        competences='Compétences requises',
        duree='3 mois',
        datePublication=timezone.now(),
        entreprise=entreprise_info,
        theme=theme_info,
        estPublie=False
    )

    salle_info = Salle.objects.create(
        numero='Salle A'
    )

    soutenance_info = Soutenance.objects.create(
        dateSoutenance=timezone.now(),
        heureSoutenance=timezone.now().time(),
        salle=salle_info,
        idContrat=contrat_info,
        candide=profil_enseignant,
        estDistanciel=False
    )

    document_info = Document.objects.create(
        titre='Titre Document',
        fichier='chemin/vers/fichier.pdf',
        contrat=contrat_info
    )

    evaluation_info = Evaluation.objects.create(
        contrat=contrat_info,
        enseignant=profil_enseignant,
        note=4.5,
        commentaire='Commentaire évaluation'
    )
    
    return HttpResponse("Données insérées avec succès !")  # Modifiez la réponse en fonction de votre utilisation de la fonction





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
          offre_list = Offre.objects.filter(estPublie=1)
          return render(request, 'etudiant/accueil_etu.html', {'offre_list': offre_list})

        if user_type == 'secretaire':
          offre_list = Offre.objects.all().order_by('-pk')
          return render(request, 'secretariat/accueil_sec.html', {'offre_list': offre_list})

        if user_type == 'enseignant':
            is_responsible = user.profilenseignant.roleEnseignant in ['chef_departement', 'enseignant_promo']
            return render(request, 'enseignant/accueil_ens.html',{'user': user, 'is_responsible': is_responsible})

    return render(request, 'pages/accueil.html')

def validation_offre(request):
    offre_list = Offre.objects.all().order_by('-pk')
    return render(request, 'secretariat/validation_offre.html', {'offre_list': offre_list})


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
            # print('////////////////////////',user_type)
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

    user_form = UtilisateurForm(request.POST)
    etudiant_form = EtudiantForm()
    enseignant_form = EnseignantForm()
    secretaire_form = SecretaireForm()

    if not user_form.is_valid():
        print('Erreurs dans le formulaire UtilisateurForm:', user_form.errors)


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
    promo_filter = request.GET.get('promo', '')

    search_mapping = {
        'ETUDIANT': (ProfilEtudiant, ['civiliteEtu', 'nomEtu', 'prenomEtu', 'numEtu', 'adresseEtu', 'cpEtu', 'villeEtu', 'telEtu', 'promo__annee', 'idDepartement__nomDep']),
        'ENTREPRISE': (Entreprise, ['nomEnt', 'numSiret', 'adresseEnt', 'cpEnt', 'villeEnt', 'responsable__nomResp', 'responsable__prenomResp', 'responsable__emailResp']),
        'CONTRAT': (Contrat, ['type', 'description', 'etat', 'dateDeb', 'dateFin', 'etudiant__civiliteEtu', 'etudiant__nomEtu', 'etudiant__prenomEtu', 'etudiant__numEtu', 'entreprise__nomEnt', 'entreprise__adresseEnt', 'entreprise__cpEnt', 'entreprise__villeEnt']),
    }

    results = []
    if search_type in search_mapping:
        model, fields = search_mapping[search_type]
        query_objects = Q()
        for field in fields:
            if field == 'promo__annee' and promo_filter:
                query_objects |= Q(**{f'{field}__icontains': promo_filter})
            else:
                query_objects |= Q(**{f'{field}__icontains': query})

        results = model.objects.filter(query_objects).values(*fields)

    if request.headers.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        data = list(results)
        return JsonResponse(data, safe=False)

    promotions = Promo.objects.all()
    return render(request, 'pages/recherche.html', {"results": results, "search_type": search_type, "promotions": promotions})

@login_required
@user_type_required('secretaire')
def contrats_non_valides(request):
    contrats_non_valides = Contrat.objects.filter(estValide__isnull=True)

    return render(request, 'secretariat/contrats_non_valides.html', {'contrats_non_valides': contrats_non_valides})

@login_required
@user_type_required('secretaire')
def valider_contrat(request, contrat_id):
    contrat = get_object_or_404(Contrat, pk=contrat_id)
    contrat.estValide = True
    contrat.etat = 0
    contrat.save()
    return redirect('lesApprentiStage:contrats_non_valides')

@login_required
@user_type_required('secretaire')
def refuser_contrat(request, contrat_id):
    contrat = get_object_or_404(Contrat, pk=contrat_id)
    contrat.estValide = False
    contrat.save()
    return redirect('lesApprentiStage:contrats_non_valides')

@login_required
def upload_convention(request):
    if request.method == 'POST':
        contrat_id = request.POST.get('contrat_id')
        fichier_upload = request.FILES.get('fichier')

        # print("Contrat ID:", contrat_id) 
        # print("Fichier:", fichier_upload)

        if fichier_upload:
            contrat = get_object_or_404(Contrat, pk=contrat_id)
            document, created = Document.objects.update_or_create(
                contrat=contrat,
                defaults={'fichier': fichier_upload, 'titre': fichier_upload.name}
            )
            contrat.etat = 1
            contrat.save()
            return HttpResponse("Fichier uploadé avec succès !")
        else:
            return HttpResponse("Aucun fichier fourni.", status=400)

    return HttpResponse("Requête invalide.", status=400)


@login_required
@user_type_required('secretaire')
def liste_contrats_signes(request):
    contrats_signes = Contrat.objects.filter(etat='1')
    for contrat in contrats_signes:
        # Supposons que vous avez une relation de un à un entre Contrat et Document
        contrat.document = Document.objects.filter(contrat=contrat).first()
    return render(request, 'secretariat/liste_contrats_signes.html', {'contrats_signes': contrats_signes})

@login_required
@user_type_required('secretaire')
def telecharger_convention_secretaire(request, document_id):
    document = get_object_or_404(Document, pk=document_id)
    response = HttpResponse(document.fichier.read(), content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    response['Content-Disposition'] = f'attachment; filename="{document.titre}"'
    return response

@login_required
@user_type_required('secretaire')
def upload_convention_secretaire(request):
    if request.method == 'POST':
        contrat_id = request.POST.get('contrat_id')
        fichier_upload = request.FILES.get('fichier')

        if fichier_upload:
            contrat = get_object_or_404(Contrat, pk=contrat_id)
            document, created = Document.objects.update_or_create(
                contrat=contrat,
                defaults={'fichier': fichier_upload, 'titre': fichier_upload.name}
            )
            contrat.etat = "2"
            contrat.save()
            return JsonResponse({'success': True, 'message': 'Fichier uploadé avec succès !'})
        else:
            return JsonResponse({'success': False, 'message': 'Aucun fichier fourni !'})
            
    return JsonResponse({'success': False, 'message': 'Méthode non autorisée.'}, status=405)


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

def ajouter_offre(request):
    if request.method == 'POST':
        form = OffreForm(request.POST)
        if form.is_valid():
            cleaned_form=form.cleaned_data
            tmp_form={
                'titre': cleaned_form.get('titre'),
                'mailRh': cleaned_form.get('mailRh'),
                'duree': cleaned_form.get('duree'),
                'description': cleaned_form.get('description'),
                'competences': cleaned_form.get('competences'),
                'entreprise': cleaned_form.get('entreprise'),
                'theme': cleaned_form.get('theme'),
                'datePublication': date.today()
            }
            form=OffreFormFini(tmp_form) 
            Offre = form.save()
            return redirect("/")
        else:
            return render(request, 'pages/ajouter_offre.html', {'OffreForm': form, 'EntrepriseForm': EntrepriseForm(), 'ThemeForm': ThemeForm()})
    else:
        form = OffreForm()

    return render(request, 'pages/ajouter_offre.html', {'OffreForm': form, 'EntrepriseForm': EntrepriseForm(), 'ThemeForm': ThemeForm()})

@login_required
def delete_offre(request, pk):
    instance = get_object_or_404(Offre, pk=pk)
    instance.delete()
    return HttpResponse("true")

@login_required
def valid_offre(request, pk):
    instance = get_object_or_404(Offre, pk=pk)
    instance.estPublie = 1
    instance.save()
    return HttpResponse("true")


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

    if query:
        queryset = queryset.filter(
            Q(titre__icontains=query) |
            Q(description__icontains=query) |
            Q(competences__icontains=query)
        )
    return render(request, 'etudiant/recherche_offres.html', {'results': queryset, 'theme': theme, 'entreprise': entreprise})


@login_required
def edit_etudiant(request):
    if request.user.type_utilisateur != 'etudiant':
        return redirect('page_d_erreur')

    profil_etudiant, created = ProfilEtudiant.objects.get_or_create(utilisateur=request.user)

    if request.method == 'POST':
        form = EtudiantProfilForm(request.POST, instance=profil_etudiant)
        if form.is_valid():
            form.save()
            messages.success(request, "Votre profil a été mis à jour avec succès.")
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

    context = {
        'etudiant': etudiant,
        'contrats': contrats,
        'documents': documents,
        'evaluations': evaluations,
        'soutenances': soutenance,
    }
    return render(request, 'etudiant/profile.html', context)

@login_required
def generer_convention_view(request, contrat_id):
    try:
        contrat = Contrat.objects.get(id=contrat_id, estValide=True, etudiant=request.user.profiletudiant)
        document_path = generer_convention(contrat)
        with open(document_path, 'rb') as doc:
            response = HttpResponse(doc.read(), content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
            response['Content-Disposition'] = f'attachment; filename="Convention_{contrat.etudiant.nomEtu}.docx"'
            return response
    except Contrat.DoesNotExist:
        return HttpResponse("Contrat non valide ou inexistant.")



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
            # Utilisez les nouvelles informations pour les étudiants
            annee = fields[0]
            nom = fields[1]
            prenom = fields[2]
            numEtu = fields[3]
            civilite = fields[4]
            adresse = fields[5]
            cp = fields[6]
            ville = fields[7]
            tel = fields[8]
            promo_nom = fields[9]
            departement_id = fields[10]

            try:
                departement = Departement.objects.get(id=departement_id)
            except Departement.DoesNotExist:
                return HttpResponse(f"Erreur : le département avec l'ID {departement_id} n'existe pas", status=400)

            username = nom + '_' + prenom
            password = make_password('password_par_defaut')
            user, created = Utilisateur.objects.get_or_create(username=username, defaults={'password': password, 'type_utilisateur': 'etudiant'})
            
            promo, created = Promo.objects.get_or_create(nomPromo=promo_nom, annee=annee, departement=departement)

            ProfilEtudiant.objects.update_or_create(
                utilisateur=user,
                nomEtu=nom,
                prenomEtu=prenom,
                numEtu=numEtu,
                civiliteEtu=civilite,
                adresseEtu=adresse,
                cpEtu=cp,
                villeEtu=ville,
                telEtu=tel,
                promo=promo,
                idDepartement=departement,
            )

    return redirect('lesApprentiStage:home')

def suivi_etudiants(request):
    user = request.user
    enseignant = ProfilEnseignant.objects.get(utilisateur=user)
    etudiants = ProfilEtudiant.objects.all()

    # Récupération des filtres
    promo_filter = request.GET.get('promo')
    entreprise_filter = request.GET.get('entreprise')
    departement_filter = request.GET.get('departement')
    theme_filter = request.GET.get('theme')
    promo_filter = request.GET.get('promo')
    statut_stage = request.GET.get('statut_stage')
    tuteur_filter = request.GET.get('tuteur')
    recherche_etudiant = request.GET.get('recherche_etudiant', '')


    if enseignant.roleEnseignant == ProfilEnseignant.CHEF_DEPARTEMENT:
        etudiants = etudiants.filter(idDepartement__chef=enseignant)
    elif enseignant.roleEnseignant == ProfilEnseignant.ENSEIGNANT_PROMO:
        promos_gerees = EnseignantPromo.objects.filter(enseignant=enseignant).values_list('promo', flat=True)
        etudiants = etudiants.filter(promo__in=promos_gerees)

    # Application des filtres
    if promo_filter:
        etudiants = etudiants.filter(promo_id=promo_filter)
    if entreprise_filter:
        etudiants = etudiants.filter(contrat__entreprise_id=entreprise_filter)
    if departement_filter:
        etudiants = etudiants.filter(idDepartement_id=departement_filter)
    if theme_filter:
        etudiants = etudiants.filter(contrat__theme_id=theme_filter)
    if statut_stage:
        if statut_stage == 'valide':
            etudiants = etudiants.filter(contrat__estValide=True)
        elif statut_stage == 'en_attente':
            etudiants = etudiants.filter(contrat__estValide=False)
        elif statut_stage == 'sans_stage':
            etudiants = etudiants.exclude(contrat__isnull=False)
    if tuteur_filter:
        etudiants = etudiants.filter(contrat__tuteur__id=tuteur_filter)
    if recherche_etudiant:
        etudiants = etudiants.filter(
            Q(nomEtu__icontains=recherche_etudiant) | 
            Q(prenomEtu__icontains=recherche_etudiant) |
            Q(numEtu__icontains=recherche_etudiant)
        )

    # Transmettre les options de filtrage au template
    promos = Promo.objects.all()
    entreprises = Entreprise.objects.all()
    departements = Departement.objects.all()
    themes = Theme.objects.all()
    tuteurs = Tuteur.objects.all()


    return render(request, 'enseignant/suivi_etudiants.html', {
        'etudiants': etudiants,
        'tuteurs': tuteurs,
        'promos': promos,
        'entreprises': entreprises,
        'departements': departements,
        'themes': themes
    })


