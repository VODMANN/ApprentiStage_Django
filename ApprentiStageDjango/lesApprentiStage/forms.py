from django import forms
from .models import Departement, Utilisateur, ProfilEtudiant, ProfilEnseignant, ProfilSecretaire

class EtudiantForm(forms.ModelForm):
    class Meta:
        model = ProfilEtudiant
        numEtu = forms.CharField(max_length=35, required=False)
        civiliteEtu = forms.CharField(max_length=5, required=False)
        adresseEtu = forms.CharField(max_length=255, required=False)
        nomEtu = forms.CharField(max_length=255, required=False)
        prenomEtu = forms.CharField(max_length=255, required=False)
        cpEtu = forms.IntegerField(required=False)
        villeEtu = forms.CharField(max_length=100, required=False)
        telEtu = forms.CharField(max_length=25, required=False)
        promo = forms.CharField(max_length=20, required=False)
        # Ajoutez un champ pour sélectionner le département si nécessaire
        idDepartement = forms.ModelChoiceField(queryset=Departement.objects.all(), required=False)
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

