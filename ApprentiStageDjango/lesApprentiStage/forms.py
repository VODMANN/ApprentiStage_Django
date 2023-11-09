from django import forms
from .models import Contrat, Departement, Entreprise, Responsable, Theme, Tuteur, Utilisateur, ProfilEtudiant, ProfilEnseignant, ProfilSecretaire

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
        idDepartement = forms.ModelChoiceField(queryset=Departement.objects.all(), required=False)
        fields = ['numEtu', 'nomEtu', 'prenomEtu', 'civiliteEtu', 'adresseEtu', 'cpEtu', 'villeEtu', 'telEtu', 'promo', 'idDepartement',]

class EnseignantForm(forms.ModelForm):
    class Meta:
        model = ProfilEnseignant
        numHarpege = forms.CharField(max_length=20, required=False)
        roleEnseignant = forms.CharField(max_length=50, required=False)
        nomEnseignant = forms.CharField(max_length=50, required=False)
        prenomEnseignant = forms.CharField(max_length=50, required=False)
        mailEnseignant = forms.EmailField(max_length=100, required=False)
        fields = ['numHarpege', 'roleEnseignant', 'nomEnseignant', 'prenomEnseignant', 'mailEnseignant',]

class SecretaireForm(forms.ModelForm):
    class Meta:
        model = ProfilSecretaire
        fields = ['numSec', ]

class DepartementForm(forms.ModelForm):
    class Meta:
        model = Departement
        nomDep = forms.CharField(max_length=100, required=False)
        adresseDep = forms.CharField(max_length=255, required=False)
        fields = ['nomDep', 'adresseDep',]

class UtilisateurForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = Utilisateur
        fields = ['username', 'password', 'type_utilisateur']

class ToggleSwitchWidget(forms.widgets.CheckboxInput):
    template_name = 'widget/toggle_switch_widget.html'


TYPE_CHOICES_CONTRAT = [
    ('Stage', 'Stage'),
    ('Apprentissage', 'Apprentissage'),
]


class ContratEtudiantForm(forms.ModelForm):
    type = forms.ChoiceField(choices=TYPE_CHOICES_CONTRAT, label='Type de Contrat')
    enFrance = forms.BooleanField(label='', widget=ToggleSwitchWidget, required=False)

    class Meta:
        model = Contrat
        exclude = ['etudiant', 'offre', 'tuteur', 'estValide','etat']

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

        labels = {
            'numSiret': 'Numéro SIRET :',
            'nomEnt': 'Nom de l\'entreprise :',
            'adresseEnt': 'Adresse :',
            'cpEnt': 'Code postal :',
            'villeEnt': 'Ville :',
        }


class ThemeForm(forms.ModelForm):
    class Meta:
        model = Theme
        fields = ['nomTheme']

        labels = {
            'nomTheme': 'Thème de votre sujet :',
            
        }


class ResponsableForm(forms.ModelForm):
    responsable_existant = forms.ModelChoiceField(
        queryset=Responsable.objects.none(), 
        required=False,
        label='Responsable Existant',
        empty_label="Ajoutez ou sélectionnez un responsable existant"
    )
    
    class Meta:
        model = Responsable
        fields = ['nomResp', 'prenomResp', 'emailResp']

    def __init__(self, *args, **kwargs):
        entreprise = kwargs.pop('entreprise', None)
        super(ResponsableForm, self).__init__(*args, **kwargs)
        if entreprise is not None:
            self.fields['responsable_existant'].queryset = Responsable.objects.filter(entreprise=entreprise)
        self.fields['nomResp'].required = False
        self.fields['prenomResp'].required = False
        self.fields['emailResp'].required = False



class TuteurForm(forms.ModelForm):
    class Meta:
        model = Tuteur
        fields = ['nomTuteur', 'prenomTuteur', 'metierTuteur', 'telTuteur', 'emailTuteur']

    def __init__(self, *args, **kwargs):
        super(TuteurForm, self).__init__(*args, **kwargs)
        