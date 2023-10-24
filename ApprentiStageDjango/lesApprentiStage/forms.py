from django import forms
from .models import Departement, Utilisateur, ProfilEtudiant, ProfilEnseignant, ProfilSecretaire

class EtudiantForm(forms.ModelForm):
    class Meta:
        model = ProfilEtudiant
        numEtu = forms.CharField(max_length=35, required=True)
        civiliteEtu = forms.CharField(max_length=5, required=True)
        adresseEtu = forms.CharField(max_length=255, required=True)
        cpEtu = forms.IntegerField(required=True)
        villeEtu = forms.CharField(max_length=100, required=True)
        telEtu = forms.CharField(max_length=25, required=True)
        promo = forms.CharField(max_length=20, required=True)
        # Ajoutez un champ pour sélectionner le département si nécessaire
        idDepartement = forms.ModelChoiceField(queryset=Departement.objects.all(), required=True)
        fields = ['numEtu', 'civiliteEtu', 'adresseEtu', 'cpEtu', 'villeEtu', 'telEtu', 'promo', 'idDepartement',]

class EnseignantForm(forms.ModelForm):
    class Meta:
        model = ProfilEnseignant
        fields = ['numHarpege', 'roleEnseignant',]

class SecretaireForm(forms.ModelForm):
    class Meta:
        model = ProfilSecretaire
        fields = ['numSec', ]

class UtilisateurForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = Utilisateur
        fields = ['username', 'password', 'type_utilisateur']

