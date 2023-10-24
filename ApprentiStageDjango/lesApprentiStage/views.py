from django.shortcuts import render, redirect
from .forms import UtilisateurForm, EtudiantForm, EnseignantForm, SecretaireForm
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse


def home(request):
  return HttpResponse('bonjour à tous')



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
                # Log in the user here if needed
                return redirect('home')
            elif user_type == 'enseignant' and enseignant_form.is_valid():
                user.save()
                enseignant = enseignant_form.save(commit=False)
                enseignant.utilisateur = user
                enseignant.save()
                # Log in the user here if needed
                return redirect('home')
            elif user_type == 'secretaire' and secretaire_form.is_valid():
                user.save()
                secretaire = secretaire_form.save(commit=False)
                secretaire.utilisateur = user
                secretaire.save()
                # Log in the user here if needed
                return redirect('home')

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
