from django import forms

from .models import Contrat, Departement, Entreprise, Promo, Responsable, Theme, Tuteur, Utilisateur, ProfilEtudiant, ProfilEnseignant, ProfilSecretaire,Soutenance, Contrat, Salle

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
        promo = forms.ModelChoiceField(queryset=Promo.objects.all(), required=False, empty_label="Sélectionnez une promo")
        idDepartement = forms.ModelChoiceField(queryset=Departement.objects.all(), required=False)
        fields = ['numEtu', 'nomEtu', 'prenomEtu', 'civiliteEtu', 'adresseEtu', 'cpEtu', 'villeEtu', 'telEtu', 'promo', 'idDepartement',]

class EnseignantForm(forms.ModelForm):
    promos = forms.ModelMultipleChoiceField(
        queryset=Promo.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'selectpicker', 'data-live-search': 'true'}),
        required=False
    )

    class Meta:
        model = ProfilEnseignant
        numHarpege = forms.CharField(max_length=20, required=False)
        roleEnseignant = forms.ChoiceField(choices=ProfilEnseignant.ROLE_CHOICES, required=False)
        nomEnseignant = forms.CharField(max_length=50, required=False)
        prenomEnseignant = forms.CharField(max_length=50, required=False)
        mailEnseignant = forms.EmailField(max_length=100, required=False)
        fields = ['numHarpege', 'roleEnseignant', 'nomEnseignant', 'prenomEnseignant', 'mailEnseignant','promos']
    
    def __init__(self, *args, **kwargs):
        super(EnseignantForm, self).__init__(*args, **kwargs)
        # Si l'instance est mise à jour, initialiser le champ 'promos'
        if self.instance and self.instance.pk:
            self.fields['promos'].initial = self.instance.promos.all()


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
    ('Apprentissage', 'Apprentissage'),
]


class ContratEtudiantForm(forms.ModelForm):
    type = forms.ChoiceField(choices=TYPE_CHOICES_CONTRAT, label='Type de Contrat')
    enFrance = forms.BooleanField(label='', widget=ToggleSwitchWidget, required=False)
    promo = forms.ModelChoiceField(queryset=Promo.objects.all(), required=False)
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
        

class EtudiantProfilForm(forms.ModelForm):
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
    promo = forms.ModelChoiceField(queryset=Promo.objects.all(), required=False, empty_label="Sélectionnez une promo")


    class Meta:
        model = ProfilEtudiant
        fields = ['numEtu', 'nomEtu', 'prenomEtu', 'adresseEtu', 'cpEtu', 'villeEtu', 'civiliteEtu','telEtu', 'idDepartement', 'promo']
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

