from django import forms

from .models import Contrat, Departement, Entreprise, Responsable, Theme, Tuteur, Utilisateur, ProfilEtudiant, ProfilEnseignant, ProfilSecretaire,Soutenance, Contrat, Salle

class EtudiantForm(forms.ModelForm):
    CIVILITE_CHOICES = [
        ('M', 'Monsieur'),
        ('Mme', 'Madame'),
    ]

    civiliteEtu = forms.ChoiceField(
        choices=CIVILITE_CHOICES,
        label='Civilité',
        required=False
    )
    cpEtu = forms.CharField(
        max_length=10,
        required=False,
        label='Code postal'
    )


    class Meta:
        model = ProfilEtudiant
        fields = ['numEtu', 'nomEtu', 'prenomEtu', 'civiliteEtu', 'adresseEtu', 'cpEtu', 'villeEtu', 'telEtu', 'promo', 'idDepartement']
        labels = {
            'numEtu': 'Numéro d\'étudiant',
            'nomEtu': 'Nom',
            'prenomEtu': 'Prénom',
            'adresseEtu': 'Adresse',
            'cpEtu': 'Code postal',
            'villeEtu': 'Ville',
            'telEtu': 'Téléphone',
            'promo': 'Promotion',
            'idDepartement': 'Département',
        }

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

class DateInput(forms.DateInput):
    input_type = 'date'


class SoutenanceForm(forms.ModelForm):
    dateSoutenance = forms.DateField(widget=DateInput())
    heureSoutenance = forms.ChoiceField(choices=HORAIRES, widget=forms.Select)
    salle = forms.ModelChoiceField(queryset=Salle.objects.all(), required=False)
    idContrat = forms.ModelChoiceField(queryset=Contrat.objects.all(), required=False)
    candide = forms.ModelChoiceField(queryset=ProfilEnseignant.objects.all(), required=False)
    estDistanciel = forms.BooleanField(required=False)
    class Meta:
        model = Soutenance
        fields = ['dateSoutenance','heureSoutenance','salle','idContrat','candide','estDistanciel']

class ToggleSwitchWidget(forms.widgets.CheckboxInput):
    template_name = 'widget/toggle_switch_widget.html'


TYPE_CHOICES_CONTRAT = [
    ('Stage', 'Stage'),
    ('Alternance', 'Alternance'),
]


class ContratEtudiantForm(forms.ModelForm):
    type = forms.ChoiceField(choices=TYPE_CHOICES_CONTRAT, label='Type de Contrat')
    enFrance = forms.BooleanField(label='', widget=ToggleSwitchWidget, required=False)

    class Meta:
        model = Contrat
        exclude = ['etudiant', 'offre', 'tuteur', 'estValide','etat','enseignant']


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
            'nomTheme': 'Theme de votre sujet :',
            
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
        
