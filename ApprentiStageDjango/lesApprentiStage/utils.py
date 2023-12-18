from io import BytesIO
from lesApprentiStage.models import Responsable
from docx import Document as DocxDocument
from .models import Document
from django.core.files.base import ContentFile
import os
from django.conf import settings

import os
from django.conf import settings

 
def remplacer_texte(doc, recherche, remplacement):
    for p in doc.paragraphs:
        if recherche in p.text:
            for run in p.runs:
                run.text = run.text.replace(recherche, remplacement)
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    for run in paragraph.runs:
                        if recherche in run.text:
                            run.text = run.text.replace(recherche, str(remplacement))


def generer_convention(contrat):
    # Charger le modèle de document Word
    doc = DocxDocument(os.path.join(settings.BASE_DIR, 'lesApprentiStage/static/MODELE_CONVENTION_STAGE.docx'))
    
    # Récupérer le responsable de l'entreprise liée au contrat
    responsable = Responsable.objects.filter(entreprise=contrat.entreprise).first()

    # Définir le contexte de remplacement
    context = {
        '{{nom_etudiant}}': contrat.etudiant.nomEtu,
        '{{prenom_etudiant}}': contrat.etudiant.prenomEtu,
        '{{nom_entreprise}}': contrat.entreprise.nomEnt,
        '{{adresse_entreprise}}': contrat.entreprise.adresseEnt,
        '{{nom_responsable}}': responsable.nomResp if responsable else '',
        '{{email_responsable}}': responsable.emailResp if responsable else '',
        '{{tel_responsable}}': responsable.telResp if responsable else '',
        '{{adresse_etudiant}}': contrat.etudiant.adresseEtu,
        '{{nom_tuteur}}': contrat.tuteur.nomTuteur,
        '{{prenom_tuteur}}': contrat.tuteur.prenomTuteur,
        '{{metier_tuteur}}': contrat.tuteur.metierTuteur,
        '{{mail_tuteur}}': contrat.tuteur.emailTuteur,
        '{{tel_tuteur}}': contrat.tuteur.telTuteur,
        '{{sexeM_etu}}': 'M ☑ ' if contrat.etudiant.civiliteEtu == 'M' else 'M ◻ ',
        '{{sexeF_etu}}': 'F ◻ ' if contrat.etudiant.civiliteEtu == 'M' else 'F ☑ ',
        '{{email_etudiant}}': contrat.etudiant.mailEtu,
        '{{tel_etudiant}}': contrat.etudiant.telEtu,
        '{{dateNaissance_etudiant}}': contrat.etudiant.dateNEtu,
        '{{titre_contrat}}': contrat.titre,
        '{{promo}}':contrat.etudiant.promo.nomPromo,
    }

    # Remplacer le texte dans les paragraphes et les tables
    for key, value in context.items():
        remplacer_texte(doc, key, value)

    # Sauvegarder le document dans un buffer en mémoire
    file_stream = BytesIO()
    doc.save(file_stream)
    file_stream.seek(0)

    # Créer un ContentFile à partir du buffer
    file_name = f'Convention_{contrat.etudiant.nomEtu}_{contrat.etudiant.prenomEtu}.docx'
    django_file = ContentFile(file_stream.read(), name=file_name)
    
    # Créer et enregistrer le nouveau document dans le modèle Document
    nouveau_document = Document(titre=file_name, fichier=django_file, contrat=contrat)
    nouveau_document.save()

    return nouveau_document.fichier.path




