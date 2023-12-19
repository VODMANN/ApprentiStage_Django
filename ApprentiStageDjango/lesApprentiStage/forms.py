from django import forms
from .models import *
from .NAF import *

class EtudiantForm(forms.ModelForm):
    mailEtu = forms.EmailField(required=False)
    numDossier = forms.IntegerField(required=False)
    ineEtu = forms.IntegerField(required=False)

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
        fields = [
                    'numEtu', 'nomEtu', 'prenomEtu', 'prenom2Etu', 'adresseEtu', 'mailEtu', 
                    'telEtu', 'dateNEtu', 'lieuNEtu', 'departementNEtu', 'nationaliteEtu', 
                    'numDossier', 'ineEtu', 'cpEtu', 'villeEtu', 'promo', 'idDepartement', 
                    'adresseParent', 'cpParent', 'villeParent', 'telParent', 'mailParent'
                ]

class EnseignantForm(forms.ModelForm):
    promos = forms.ModelMultipleChoiceField(
        queryset=Promo.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'selectpicker col', 'data-live-search': 'true'}),
        required=False
    )
    departements = forms.ModelChoiceField(
        queryset=Departement.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'selectpicker col', 'data-live-search': 'true'})
    )
    telEnseignant = forms.CharField(max_length=25, required=False)
    disciplineEnseignant = forms.CharField(max_length=150, required=False)



    class Meta:
        model = ProfilEnseignant
        numHarpege = forms.CharField(max_length=20, required=False)
        roleEnseignant = forms.ChoiceField(choices=ProfilEnseignant.ROLE_CHOICES, required=False)
        nomEnseignant = forms.CharField(max_length=50, required=False)
        prenomEnseignant = forms.CharField(max_length=50, required=False)
        mailEnseignant = forms.EmailField(max_length=100, required=False)
        fields = ['numHarpege', 'roleEnseignant', 'nomEnseignant', 'prenomEnseignant',
                  'mailEnseignant', 'telEnseignant', 'disciplineEnseignant',
                  'promos', 'departements']

        labels = {
            'promos': 'Promos :',
            'departements': 'Département :'
        }

    def __init__(self, *args, **kwargs):
        super(EnseignantForm, self).__init__(*args, **kwargs)
        # Si l'instance est mise à jour, initialiser le champ 'promos'
        if self.instance and self.instance.pk:
            self.fields['promos'].initial = self.instance.promos.all()



class Enseignant_secForm(forms.ModelForm):
    promos = forms.ModelMultipleChoiceField(
        queryset=Promo.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'selectpicker col', 'data-live-search': 'true'}),
        required=False
    )
    departements = forms.ModelChoiceField(
        queryset=Departement.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'selectpicker col', 'data-live-search': 'true'})
    )
    telEnseignant = forms.CharField(max_length=25, required=False)
    disciplineEnseignant = forms.CharField(max_length=150, required=False)



    class Meta:
        model = ProfilEnseignant
        numHarpege = forms.CharField(max_length=20, required=False)
        roleEnseignant = forms.ChoiceField(choices=ProfilEnseignant.ROLE_CHOICES, required=False)
        nomEnseignant = forms.CharField(max_length=50, required=False)
        prenomEnseignant = forms.CharField(max_length=50, required=False)
        mailEnseignant = forms.EmailField(max_length=100, required=False)
        fields = ['numHarpege', 'roleEnseignant', 'nomEnseignant', 'prenomEnseignant',
                  'mailEnseignant', 'telEnseignant', 'disciplineEnseignant',
                  'promos', 'departements']

        labels = {
            'promos': 'Promos :',
            'departements': 'Département :'
        }

    def __init__(self, *args, **kwargs):
        super(Enseignant_secForm, self).__init__(*args, **kwargs)  # Correction ici
        if self.instance and self.instance.pk:
            self.fields['promos'].initial = [ep.promo for ep in EnseignantPromo.objects.filter(enseignant=self.instance)]






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
    codeNaf = forms.ChoiceField(choices=NAF, required=False)
    
    class Meta:
        model = Entreprise
        fields = ['numSiret', 'nomEnt', 'adresseEnt', 'codeNaf', 'cpEnt', 'villeEnt', 'formeJuridique', 'telEnt', 'siteWeb', 'numSiren', 'mailEnt']
        labels = {
            'numSiret': 'Numéro SIRET :',
            'nomEnt': 'Nom de l\'entreprise :',
            'adresseEnt': 'Adresse :',
            'cpEnt': 'Code postal :',
            'villeEnt': 'Ville :',
            'formeJuridique': 'Forme juridique :',
            'telEnt': 'Téléphone :',
            'siteWeb': 'Site Web :',
            'numSiren': 'Numéro SIREN :',
            'mailEnt': 'Email :',
            'codeNaf': 'Code NAF :',
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
        fields = ['nomResp', 'prenomResp', 'emailResp', 'posteResp', 'telResp']

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

    def __init__(self, *args, **kwargs):
        super(EtudiantProfilForm, self).__init__(*args, **kwargs)
        # Mettre les champs numDossier et ineEtu en lecture seule
        self.fields['numDossier'].widget.attrs['readonly'] = True
        self.fields['ineEtu'].widget.attrs['readonly'] = True


    class Meta:
        model = ProfilEtudiant
        fields = [
            'numEtu', 'nomEtu', 'prenomEtu', 'prenom2Etu', 'adresseEtu', 'cpEtu', 'villeEtu', 'civiliteEtu',
            'mailEtu', 'telEtu', 'dateNEtu', 'lieuNEtu', 'departementNEtu', 'nationaliteEtu', 'numDossier',
            'ineEtu', 'promo', 'idDepartement', 'adresseParent', 'cpParent', 'villeParent', 'telParent',
            'mailParent'
        ]
        labels = {
        'numEtu': 'Numéro d\'étudiant',
        'nomEtu': 'Nom',
        'prenomEtu': 'Prénom',
        'prenom2Etu': 'Deuxième prénom',
        'adresseEtu': 'Adresse',
        'cpEtu': 'Code postal',
        'villeEtu': 'Ville',
        'civiliteEtu': 'Civilité',
        'mailEtu': 'E-mail',
        'telEtu': 'Téléphone',
        'dateNEtu': 'Date de naissance',
        'lieuNEtu': 'Lieu de naissance',
        'departementNEtu': 'Département de naissance',
        'nationaliteEtu': 'Nationalité',
        'numDossier': 'Numéro de dossier',
        'ineEtu': 'Numéro INE',
        'promo': 'Promotion',
        'idDepartement': 'Département',
        'adresseParent': 'Adresse des parents',
        'cpParent': 'Code postal des parents',
        'villeParent': 'Ville des parents',
        'telParent': 'Téléphone des parents',
        'mailParent': 'E-mail des parents'
    }



class OffreForm(forms.ModelForm):

    class Meta:
        model = Offre
        fields = ['titre','mailRh','duree','description','competences','entreprise','theme']
        widgets = {
          'description': forms.Textarea(attrs={'rows':4}),
          'competences': forms.Textarea(attrs={'rows':4}),
        }
        labels = {
            'titre': 'Titre',
            'description': 'Description',
            'mailRh': 'Mail',
            'competences': 'Compétences',
            'duree': 'Durée',
            'entreprise': "Entreprise",
            'theme': 'Thème',
        }
        
        
class OffreFormFini(forms.ModelForm):

    class Meta:
        model = Offre
        fields = ['titre','mailRh','duree','description','competences','entreprise','theme','datePublication']



class ConventionUploadForm(forms.Form):
    fichier = forms.FileField(label='Sélectionnez votre fichier')

class ContratForm(forms.ModelForm):
    class Meta:
        model = Contrat
        fields = ['type', 'titre', 'description', 'etat', 'gratification', 'dateDeb', 'dateFin', 'etudiant', 'enseignant', 'tuteur', 'theme', 'entreprise', 'enFrance']



class ProfilEnseignantForm(forms.ModelForm):
    class Meta:
        model = ProfilEnseignant
        fields = ['nomEnseignant', 'prenomEnseignant', 'telEnseignant', 'mailEnseignant', 'roleEnseignant', 'disciplineEnseignant']
        # Ajoutez d'autres champs si nécessaire
        labels = {
            'nomEnseignant': 'Nom',
            'prenomEnseignant': 'Prénom',
            # Ajoutez d'autres étiquettes pour les champs ici
        }