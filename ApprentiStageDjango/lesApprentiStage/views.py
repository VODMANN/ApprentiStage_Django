from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ContratEtudiantForm, EntrepriseForm, ResponsableForm, ThemeForm, TuteurForm, UtilisateurForm, EtudiantForm, EnseignantForm, SecretaireForm
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.contrib.auth.views import LoginView
from .models import ProfilEtudiant, Entreprise, Contrat, Utilisateur
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required

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
                from django.contrib.auth.views import redirect_to_login
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

""" @login_required
@user_type_required('secretaire') """
def signup(request):
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


# def ajouter_responsable(request, contrat_id):
#     contrat = get_object_or_404(Contrat, pk=contrat_id)
#     entreprise = contrat.entreprise

#     if request.method == 'POST':
#         form = ResponsableForm(request.POST, entreprise=entreprise)
#         if form.is_valid():
#             if form.cleaned_data['responsable_existant']:
#                 contrat.responsable = form.cleaned_data['responsable_existant']
#                 contrat.save()
#                 messages.success(request, "Responsable lié au contrat avec succès.")
#             else:
#                 responsable = form.save(commit=False)
#                 responsable.entreprise = entreprise
#                 responsable.save()
#                 contrat.responsable = responsable
#                 contrat.save()
#                 messages.success(request, "Responsable ajouté avec succès.")
#             return redirect('lesApprentiStage:home')
#     else:
#         form = ResponsableForm(entreprise=entreprise)

#     return render(request, 'pages/ajouter_responsable.html', {'form': form})

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
    context = {
        'contrat': contrat,
    }
    return render(request, 'admin/affichageContrat.html', context)
