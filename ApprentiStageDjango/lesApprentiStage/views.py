from django.shortcuts import render, redirect
from .forms import UtilisateurForm, EtudiantForm, EnseignantForm, SecretaireForm
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.contrib.auth.views import LoginView
from .models import ProfilEtudiant, Entreprise, Contrat

class UserLoginView(LoginView):
    template_name = 'registration/login.html'

def home(request):
  if request.user.is_authenticated:
        user_type = request.user.type_utilisateur
        print(user_type)
  return render(request, 'pages/accueil.html')

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

def pageRecherche(request):
    return render(request, 'pages/recherche.html')

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
