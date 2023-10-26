from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UtilisateurForm, EtudiantForm, EnseignantForm, SecretaireForm,SoutenanceForm
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.views import LoginView
from .models import ProfilEtudiant, Entreprise, Contrat,Soutenance,Salle
from django.contrib.auth.views import redirect_to_login

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
    if request.method == 'POST':
        formSoutenance = SoutenanceForm(request.POST)
        if formSoutenance.is_valid():
            if 'ajouter' in request.POST:
                verification = Soutenance.objects.filter(salle = formSoutenance.cleaned_data['salle'], heureSoutenance = formSoutenance.cleaned_data['heureSoutenance'],dateSoutenance = formSoutenance.cleaned_data['dateSoutenance'])
                if len(verification)==0:
                    uneSoutenance = formSoutenance.save(commit=False)
                    uneSoutenance.save()
                return redirect('lesApprentiStage:soutenance')
    else:
        formSoutenance = SoutenanceForm()
    listSoutenance = Soutenance.objects.all()
    return render(request, 'pages/soutenance.html',{"form": formSoutenance,'listSoutenance': listSoutenance})

@login_required
def supprimerSoutenance(request,id):
    unesoutenance = Soutenance.objects.filter(id = id)[0]
    unesoutenance.delete()
    return redirect('lesApprentiStage:soutenance')

@login_required
def modifierSoutenance(request,id):
    unesoutenance = Soutenance.objects.filter(id = id)[0]
    listSoutenance = Soutenance.objects.all()
    if request.method == 'POST':
        formSoutenance = SoutenanceForm(request.POST)
        if formSoutenance.is_valid():
             if 'modifier' in request.POST:
                verification = Soutenance.objects.filter(salle = formSoutenance.cleaned_data['salle'], heureSoutenance = formSoutenance.cleaned_data['heureSoutenance'],dateSoutenance = formSoutenance.cleaned_data['dateSoutenance'])
                if len(verification)==0:
                    unesoutenance.dateSoutenance = formSoutenance.cleaned_data['dateSoutenance']
                    unesoutenance.heureSoutenance = formSoutenance.cleaned_data['heureSoutenance']
                    unesoutenance.salle = formSoutenance.cleaned_data['salle']
                    unesoutenance.idContrat = formSoutenance.cleaned_data['idContrat']
                    unesoutenance.candide = formSoutenance.cleaned_data['candide']
                    unesoutenance.estDistanciel = formSoutenance.cleaned_data['estDistanciel']
                    unesoutenance.save()
                return redirect('lesApprentiStage:soutenance')
    else:
        formSoutenance = SoutenanceForm(initial={'dateSoutenance': unesoutenance.dateSoutenance,'heureSoutenance': unesoutenance.heureSoutenance, 'salle': unesoutenance.salle, 'idContrat': unesoutenance.idContrat, 'candide': unesoutenance.candide, 'estDistanciel': unesoutenance.estDistanciel})
    return render(request, 'pages/soutenance.html',{"form": formSoutenance,'listSoutenance': listSoutenance, 'modifSoutenance': unesoutenance})