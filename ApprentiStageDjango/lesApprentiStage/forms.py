from django import forms
from .models import Departement, Utilisateur, ProfilEtudiant, ProfilEnseignant, ProfilSecretaire,Soutenance,Contrat,Salle
class EtudiantForm(forms.ModelForm):
    class Meta:
        model = ProfilEtudiant
        numEtu = forms.CharField(max_length=35, required=False)
        nomEtu = forms.CharField(max_length=255, required=False)
        prenomEtu = forms.CharField(max_length=255, required=False)
        civiliteEtu = forms.CharField(max_length=5, required=False)
        cpEtu = forms.IntegerField(required=False)
        villeEtu = forms.CharField(max_length=100, required=False)
        telEtu = forms.CharField(max_length=25, required=False)
        promo = forms.CharField(max_length=20, required=False)
        # Ajoutez un champ pour sélectionner le département si nécessaire
        idDepartement = forms.ModelChoiceField(queryset=Departement.objects.all(), required=False)
        fields = ['numEtu', 'nomEtu', 'prenomEtu', 'civiliteEtu', 'adresseEtu', 'cpEtu', 'villeEtu', 'telEtu', 'promo', 'idDepartement',]

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


HORAIRES = (("09:00:00","9h"),("10:00:00","10h"),("11:00:00","11h"),("14:00:00","14h"),("15:00:00","15h"),("16:00:00","16h"),)

class SoutenanceForm(forms.ModelForm):
    dateSoutenance = forms.DateField()
    heureSoutenance = forms.ChoiceField(choices=HORAIRES,widget=forms.Select)
    salle = forms.ModelChoiceField(queryset=Salle.objects.all(), required=False)
    idContrat = forms.ModelChoiceField(queryset=Contrat.objects.all(), required=False)
    candide = forms.ModelChoiceField(queryset=ProfilEnseignant.objects.all(), required=False)
    estDistanciel = forms.BooleanField(required=False)
    class Meta:
        model = Soutenance
        fields = ['dateSoutenance','heureSoutenance','salle','idContrat','candide','estDistanciel']