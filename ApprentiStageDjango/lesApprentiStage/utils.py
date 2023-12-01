from lesApprentiStage.models import Responsable
from docx import Document
import os
from django.conf import settings

def generer_convention(contrat):
    doc = Document(os.path.join(settings.BASE_DIR, '/home/rochdi/iut/v2/ApprentiStage_Django/ApprentiStageDjango/lesApprentiStage/static/MODELE_CONVENTION_STAGE.docx'))
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

    save_path = os.path.join(save_dir, f'Convention_{contrat.etudiant.nomEtu}_{contrat.etudiant.prenomEtu}.docx')
    doc.save(save_path)

    return save_path
