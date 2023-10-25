from django import forms
from .models import Contrat, Departement, Entreprise, Utilisateur, ProfilEtudiant, ProfilEnseignant, ProfilSecretaire

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



TYPE_CHOICES_CONTRAT = [
    ('Stage', 'Stage'),
    ('Alternance', 'Alternance'),
]


class ContratEtudiantForm(forms.ModelForm):
    type = forms.ChoiceField(choices=TYPE_CHOICES_CONTRAT, label='Type de Contrat')
    class Meta:
        model = Contrat
        exclude = ['etudiant', 'offre', 'tuteur', 'estValide']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ContratEtudiantForm, self).__init__(*args, **kwargs)
        if user and hasattr(user, 'profiletudiant'):
            self.fields['etudiant'].initial = user.profilEtudiant.numEtu
            self.instance.etudiant = user.profilEtudiant


class EntrepriseForm(forms.ModelForm):
    class Meta:
        model = Entreprise
        fields = ['numSiret', 'nomEnt', 'adresseEnt', 'cpEnt', 'villeEnt']
