from django import forms
from django_filters import rest_framework as filters
import django_filters
from .models import *
from django.forms.widgets import DateInput, TimeInput

TYPE_CHOICES_CONTRAT = [
    ('Stage', 'Stage'),
    ('Apprentissage', 'Apprentissage'),
]

ETAT_CHOICES_CONTRAT = [
    (0, 'non signé'),
    (1, 'signé par etudiant/entreprise'),
    (2, 'sifné par tous'),
]

class ContratFilter(filters.FilterSet):
    type = django_filters.ChoiceFilter(choices=TYPE_CHOICES_CONTRAT, label='Type de Contrat')
    etat = django_filters.ChoiceFilter(choices=ETAT_CHOICES_CONTRAT)
    etudiant__nomEtu = django_filters.CharFilter(lookup_expr='icontains', label='Nom Etudiant')
    etudiant__prenomEtu = django_filters.CharFilter(lookup_expr='icontains', label='Prenom Etudiant')
    entreprise__nomEnt = django_filters.CharFilter(lookup_expr='icontains', label='Nom Entreprise')
    theme__nomTheme = django_filters.CharFilter(lookup_expr='icontains', label='Nom Theme')

    class Meta:
        model = Contrat
        fields = ['type', 'etat', 'etudiant__nomEtu', 'etudiant__prenomEtu', 'entreprise__nomEnt', 'theme__nomTheme']

class ProfilEtudiantFilter(filters.FilterSet):
    nomEtu = django_filters.CharFilter(lookup_expr='icontains', label='Nom Etudiant')
    prenomEtu = django_filters.CharFilter(lookup_expr='icontains', label='Prénom Etudiant')
    numEtu = django_filters.CharFilter(lookup_expr='icontains', label='Numéro Etudiant')
    promo__nomPromo = django_filters.ModelChoiceFilter(
        queryset=Promo.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Promo'
    )
        
    class Meta:
        model = ProfilEtudiant
        fields = ['nomEtu', 'prenomEtu', 'numEtu', 'promo__nomPromo', 'idDepartement__nomDep']

class ProfilEnseignantFilter(filters.FilterSet):
    numHarpege = django_filters.CharFilter(lookup_expr='icontains', label='Numéro Harpège')
    nomEnseignant = django_filters.CharFilter(lookup_expr='icontains', label='Nom de l\'enseignant')
    prenomEnseignant = django_filters.CharFilter(lookup_expr='icontains', label='Prénom de l\'enseignant')
    roleEnseignant = django_filters.CharFilter(lookup_expr='icontains', label='Rôle de l\'enseignant')
    disciplineEnseignant = django_filters.CharFilter(lookup_expr='icontains', label='Discipline de l\'enseignant')

    class Meta:
        model = ProfilEnseignant
        fields = ['numHarpege', 'nomEnseignant', 'prenomEnseignant', 'roleEnseignant', 'disciplineEnseignant']

class PromoFilter(filters.FilterSet):
    nomPromo = django_filters.CharFilter(lookup_expr='icontains', label='Nom de la promotion')
    anneeScolaire = django_filters.CharFilter(lookup_expr='icontains', label='Année Scolaire')
    departement__nomDep = django_filters.CharFilter(lookup_expr='icontains', label='Nom du département')

    class Meta:
        model = Promo
        fields = ['nomPromo', 'anneeScolaire', 'departement__nomDep']



class EntrepriseFilter(filters.FilterSet):
    nomEnt = django_filters.CharFilter(lookup_expr='icontains', label='Nom de l\'entreprise')
    mailEnt = django_filters.CharFilter(lookup_expr='icontains', label='Email de l\'entreprise')
    codeNaf = django_filters.CharFilter(lookup_expr='icontains', label='Code NAF')
    villeEnt = django_filters.CharFilter(lookup_expr='icontains', label='Ville de l\'entreprise')

    class Meta:
        model = Entreprise
        fields = ['nomEnt', 'mailEnt', 'codeNaf', 'villeEnt']

class ThemeFilter(filters.FilterSet):
    nomTheme = django_filters.CharFilter(lookup_expr='icontains', label='Nom du thème')

    class Meta:
        model = Theme
        fields = ['nomTheme']

class SalleFilter(filters.FilterSet):
    numero = django_filters.CharFilter(lookup_expr='icontains', label='Numéro de la salle')

    class Meta:
        model = Salle
        fields = ['numero']

class DepartementFilter(filters.FilterSet):
    nomDep = django_filters.CharFilter(lookup_expr='icontains', label='Nom du département')
    adresseDep = django_filters.CharFilter(lookup_expr='icontains', label='Adresse du département')

    class Meta:
        model = Departement
        fields = ['nomDep', 'adresseDep']

class ResponsableFilter(filters.FilterSet):
    nomResp = django_filters.CharFilter(lookup_expr='icontains', label='Nom du responsable')
    prenomResp = django_filters.CharFilter(lookup_expr='icontains', label='Prénom du responsable')
    emailResp = django_filters.CharFilter(lookup_expr='icontains', label='Email du responsable')
    posteResp = django_filters.CharFilter(lookup_expr='icontains', label='Poste du responsable')

    class Meta:
        model = Responsable
        fields = ['nomResp', 'prenomResp', 'emailResp', 'posteResp']



class TuteurFilter(filters.FilterSet):
    nomTuteur = django_filters.CharFilter(lookup_expr='icontains', label='Nom du tuteur')
    prenomTuteur = django_filters.CharFilter(lookup_expr='icontains', label='Prénom du tuteur')
    metierTuteur = django_filters.CharFilter(lookup_expr='icontains', label='Métier du tuteur')
    emailTuteur = django_filters.CharFilter(lookup_expr='icontains', label='Email du tuteur')

    class Meta:
        model = Tuteur
        fields = ['nomTuteur', 'prenomTuteur', 'metierTuteur', 'emailTuteur']

class OffreFilter(filters.FilterSet):
    titre = django_filters.CharFilter(lookup_expr='icontains', label='Titre de l\'offre')
    competences = django_filters.CharFilter(lookup_expr='icontains', label='Compétences requises')
    datePublication = django_filters.CharFilter(lookup_expr='icontains', label='Date de publication')
    entreprise__nomEnt = django_filters.CharFilter(lookup_expr='icontains', label='Nom de l\'entreprise')
    theme__nomTheme = django_filters.CharFilter(lookup_expr='icontains', label='Nom du thème')

    class Meta:
        model = Offre
        fields = ['titre', 'competences', 'datePublication', 'entreprise__nomEnt', 'theme__nomTheme']

class SoutenanceFilter(filters.FilterSet):
    dateSoutenance = django_filters.DateFilter(
        widget=DateInput(attrs={'type': 'date'}),
        label='Date de soutenance'
    )
    heureSoutenance = django_filters.TimeFilter(
        widget=TimeInput(attrs={'type': 'time'}),
        label='Heure de soutenance'
    )
    salle__numero = django_filters.CharFilter(lookup_expr='icontains', label='Numéro de salle')
    idContrat__etudiant__nomEtu = django_filters.CharFilter(lookup_expr='icontains', label='Nom de l\'étudiant')
    idContrat__etudiant__prenomEtu = django_filters.CharFilter(lookup_expr='icontains', label='Prénom de l\'étudiant')
    estDistanciel = django_filters.CharFilter(lookup_expr='icontains', label='Est distanciel')
    idContrat__etudiant__promo = django_filters.ModelChoiceFilter(
        queryset=Promo.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Promo'
    )

    class Meta:
        model = Soutenance
        fields = ['dateSoutenance', 'heureSoutenance', 'salle__numero', 'idContrat__etudiant__nomEtu', 'idContrat__etudiant__prenomEtu', 'estDistanciel', 'idContrat__etudiant__promo']


class DocumentFilter(filters.FilterSet):
    titre = django_filters.CharFilter(lookup_expr='icontains', label='Titre du document')
    contrat__etudiant__nomEtu = django_filters.CharFilter(lookup_expr='icontains', label='Nom de l\'étudiant')
    contrat__etudiant__prenomEtu = django_filters.CharFilter(lookup_expr='icontains', label='Prénom de l\'étudiant')

    class Meta:
        model = Document
        fields = ['titre', 'contrat__etudiant__nomEtu', 'contrat__etudiant__prenomEtu']

class EvaluationFilter(filters.FilterSet):
    contrat__etudiant__nomEtu = django_filters.CharFilter(lookup_expr='icontains', label='Nom de l\'étudiant')
    contrat__etudiant__prenomEtu = django_filters.CharFilter(lookup_expr='icontains', label='Prénom de l\'étudiant')
    enseignant__nomEnseignant = django_filters.CharFilter(lookup_expr='icontains', label='Nom de l\'enseignant')
    enseignant__prenomEnseignant = django_filters.CharFilter(lookup_expr='icontains', label='Prénom de l\'enseignant')

    class Meta:
        model = Evaluation
        fields = ['contrat__etudiant__nomEtu', 'contrat__etudiant__prenomEtu', 'enseignant__nomEnseignant', 'enseignant__prenomEnseignant']

class EtablissementFilter(filters.FilterSet):
    nomUniversite = django_filters.CharFilter(lookup_expr='icontains', label='Nom de l\'université')
    adresseUniversite = django_filters.CharFilter(lookup_expr='icontains', label='Adresse de l\'université')
    villeEtablissement = django_filters.CharFilter(lookup_expr='icontains', label='Ville de l\'établissement')
    telEtablissement = django_filters.CharFilter(lookup_expr='icontains', label='Téléphone de l\'établissement')
    mailEtablissement = django_filters.CharFilter(lookup_expr='icontains', label='Email de l\'établissement')
    siretEtablissement = django_filters.CharFilter(lookup_expr='icontains', label='SIRET de l\'établissement')
    nomEtablissement = django_filters.CharFilter(lookup_expr='icontains', label='Nom de l\'établissement')
    directeurEtablissement = django_filters.CharFilter(lookup_expr='icontains', label='Directeur de l\'établissement')

    class Meta:
        model = Etablissement
        fields = ['nomUniversite', 'adresseUniversite', 'villeEtablissement', 'telEtablissement', 'mailEtablissement', 'siretEtablissement', 'nomEtablissement', 'directeurEtablissement']