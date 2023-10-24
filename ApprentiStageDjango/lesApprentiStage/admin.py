from django.contrib import admin
from .models import Utilisateur, ProfilEtudiant, ProfilEnseignant, ProfilSecretaire, Departement,Enseignant,Entreprise,Theme,Etudiant,Responsable,Tuteur,Contrat,Offre

admin.site.register(Utilisateur)
admin.site.register(ProfilEtudiant)
admin.site.register(ProfilEnseignant)
admin.site.register(ProfilSecretaire)
admin.site.register(Departement)
admin.site.register(Enseignant)
admin.site.register(Entreprise)
admin.site.register(Theme)
admin.site.register(Tuteur)
admin.site.register(Responsable)
admin.site.register(Contrat)
admin.site.register(Offre)
admin.site.register(Etudiant)

