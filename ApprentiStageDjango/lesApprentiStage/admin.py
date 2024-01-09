from django.contrib import admin
from .models import *

admin.site.register(Utilisateur)
admin.site.register(ProfilEtudiant)
admin.site.register(ProfilEnseignant)
admin.site.register(ProfilSecretaire)
admin.site.register(Departement)
admin.site.register(Entreprise)
admin.site.register(Theme)
admin.site.register(Tuteur)
admin.site.register(Responsable)
admin.site.register(Contrat)
admin.site.register(Offre)
admin.site.register(Promo)
admin.site.register(Document)

admin.site.register(Soutenance)
admin.site.register(NombreSoutenances)
