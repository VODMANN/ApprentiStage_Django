from django import forms
from django_filters import rest_framework as filters
import django_filters
from .models import *

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
    class Meta:
        model = ProfilEnseignant
        fields = ['numHarpege', 'nomEnseignant', 'prenomEnseignant', 'roleEnseignant', 'disciplineEnseignant']

class PromoFilter(filters.FilterSet):
    class Meta:
        model = Promo
        fields = ['nomPromo', 'annee', 'departement__nomDep']

class EntrepriseFilter(filters.FilterSet):
    class Meta:
        model = Entreprise
        fields = ['nomEnt', 'mailEnt', 'codeNaf', 'villeEnt']

class ThemeFilter(filters.FilterSet):
    class Meta:
        model = Theme
        fields = ['nomTheme']
        
class SalleFilter(filters.FilterSet):
    class Meta:
        model = Salle
        fields = ['numero']

class DepartementFilter(filters.FilterSet):
    class Meta:
        model = Departement
        fields = ['nomDep']

class ResponsableFilter(filters.FilterSet):
    class Meta:
        model = Responsable
        fields = ['nomResp', 'prenomResp', 'emailResp', 'posteResp']

class TuteurFilter(filters.FilterSet):
    class Meta:
        model = Tuteur
        fields = ['nomTuteur', 'prenomTuteur', 'metierTuteur', 'emailTuteur']

class OffreFilter(filters.FilterSet):
    class Meta:
        model = Offre
        fields = ['titre', 'competences', 'datePublication', 'entreprise__nomEnt', 'theme__nomTheme']

class SoutenanceFilter(filters.FilterSet):
    class Meta:
        model = Soutenance
        fields = ['dateSoutenance', 'heureSoutenance', 'salle__numero', 'idContrat__etudiant__nomEtu', 'idContrat__etudiant__prenomEtu', 'estDistanciel']

class DocumentFilter(filters.FilterSet):
    class Meta:
        model = Document
        fields = ['titre', 'contrat__etudiant__nomEtu', 'contrat__etudiant__prenomEtu']

class EvaluationFilter(filters.FilterSet):
    class Meta:
        model = Evaluation
        fields = ['contrat__etudiant__nomEtu', 'contrat__etudiant__prenomEtu', 'enseignant__nomEnseignant', 'enseignant__prenomEnseignant']

class EtablissementFilter(filters.FilterSet):
    class Meta:
        model = Etablissement
        fields = ['nomUniversite', 'adresseUniversite', 'villeEtablissement', 'telEtablissement', 'mailEtablissement', 'siretEtablissement', 'nomEtablissement', 'directeurEtablissement']
