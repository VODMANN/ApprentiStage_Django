from lesApprentiStage.models import Responsable
from django.core.files import File
from docx import Document as Documents
from .models import *
from django.core.files.base import ContentFile

import os
from django.conf import settings


def remplacer_texte(doc, recherche, remplacement):
    for p in doc.paragraphs:
        if recherche in p.text:
            for run in p.runs:
                run.text = run.text.replace(recherche, remplacement)

def generer_convention(contrat):
    doc = Documents(os.path.join(settings.BASE_DIR, '/home/rochdi/iut/v2/ApprentiStage_Django/ApprentiStageDjango/lesApprentiStage/static/MODELE_CONVENTION_STAGE.docx'))
    responsable = Responsable.objects.filter(entreprise=contrat.entreprise).first()

    context = {
    '{{ nom_etudiant }}': contrat.etudiant.nomEtu,
    '{{ prenom_etudiant }}': contrat.etudiant.prenomEtu,
    '{{ nom_entreprise }}': contrat.entreprise.nomEnt,
    '{{ adresse_entreprise }}': contrat.entreprise.adresseEnt,
    '{{ nom_responsable }}': responsable.nomResp if responsable else '',
    '{{ email_responsable }}': responsable.emailResp if responsable else '',
    '{{ adresse_etudiant }}': contrat.etudiant.adresseEtu,
    '{{ nom_tuteur }}': contrat.tuteur.nomTuteur,
    '{{ prenom_tuteur }}': contrat.tuteur.prenomTuteur,
    '{{ metier_tuteur }}': contrat.tuteur.metierTuteur,
    '{{ mail_tuteur }}': contrat.tuteur.emailTuteur,
    '{{ sexeM_etu }}': 'M ☑ ' if contrat.etudiant.civiliteEtu == 'M.' else 'M ◻ ',
    '{{ sexeF_etu }}': 'F ◻ ' if contrat.etudiant.civiliteEtu == 'M.' else 'F ☑ ',
    }

    # Remplacement dans les paragraphes
    for p in doc.paragraphs:
        for key, value in context.items():
            if key in p.text:
                p.text = p.text.replace(key, value)

    # Remplacement dans les tables
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for key, value in context.items():
                    if key in cell.text:
                        cell.text = cell.text.replace(key, value)



    save_dir = os.path.join(settings.MEDIA_ROOT, 'conventions')
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    file_name = f'Convention_{contrat.etudiant.nomEtu}_{contrat.etudiant.prenomEtu}.docx'
    save_path = os.path.join(settings.MEDIA_ROOT, 'documents', 'conventions', file_name)

    doc.save(save_path)

    with open(save_path, 'rb') as file:
        django_file = ContentFile(file.read(), name=file_name)
        nouveau_document = Document(titre=file_name, fichier=django_file, contrat=contrat)
        # Sauvegardez le document pour enregistrer le fichier dans MEDIA_ROOT
        nouveau_document.save()

    return save_path

