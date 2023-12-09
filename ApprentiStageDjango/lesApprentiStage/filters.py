from django_filters import rest_framework as filters
import django_filters
from .models import *

TYPE_CHOICES_CONTRAT = [
    ('Stage', 'Stage'),
    ('Apprentissage', 'Apprentissage'),
]

ETAT_CHOICES_CONTRAT = [
    (0,'non signé'),
    (1,'signé par etudiant/entreprise'),
    (2,'sifné par tous'),

]

class ContratFilter(filters.FilterSet):
    type = django_filters.ChoiceFilter(choices=TYPE_CHOICES_CONTRAT, label='Type de Contrat')
    etat = django_filters.ChoiceFilter(choices=ETAT_CHOICES_CONTRAT)

    class Meta:
        model = Contrat
        fields = ['type', 'etat', 'etudiant__nomEtu', 'etudiant__prenomEtu', 'entreprise__nomEnt', 'theme__nomTheme']
