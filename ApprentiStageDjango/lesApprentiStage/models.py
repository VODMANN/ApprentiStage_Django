from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

class Utilisateur(AbstractUser):
    TYPE_CHOICES = (
        ('etudiant', 'Etudiant'),
        ('enseignant', 'Enseignant'),
        ('secretaire', 'Secrétaire'),
    )
    type_utilisateur = models.CharField(max_length=10, choices=TYPE_CHOICES, default='etudiant')

class ProfilEtudiant(models.Model):
    utilisateur = models.OneToOneField(Utilisateur, on_delete=models.CASCADE)
    nomEtu = models.CharField(max_length=50,null=True)
    prenomEtu = models.CharField(max_length=50,null=True)
    numEtu = models.CharField(max_length=35, primary_key=True)
    civiliteEtu = models.CharField(max_length=5,null=True)
    adresseEtu = models.CharField(max_length=255,null=True)
    cpEtu = models.IntegerField(null=True)
    villeEtu = models.CharField(max_length=100,null=True)
    telEtu = models.CharField(max_length=25,null=True)
    promo = models.CharField(max_length=20,null=True)
    idDepartement = models.ForeignKey('Departement', on_delete=models.CASCADE)

    def __str__(self):
        return self.utilisateur.username

class ProfilEnseignant(models.Model):
    utilisateur = models.OneToOneField(Utilisateur, on_delete=models.CASCADE)
    numHarpege = models.CharField(max_length=20, primary_key=True)
    roleEnseignant = models.CharField(max_length=50, null=True)
    nomEnseignant = models.CharField(max_length=50, null=True)
    prenomEnseignant = models.CharField(max_length=50, null=True)
    mailEnseignant = models.EmailField(max_length=100, null=True)

    def __str__(self):
        return self.utilisateur.username

class ProfilSecretaire(models.Model):
    utilisateur = models.OneToOneField(Utilisateur, on_delete=models.CASCADE)
    numSec= models.CharField(max_length=20, null=True)

    def __str__(self):
        return self.utilisateur.username

class Departement(models.Model):
    nomDep = models.CharField(max_length=100)
    adresseDep = models.CharField(max_length=255)

    def __str__(self):
        return self.nomDep

class Entreprise(models.Model):
    numSiret = models.CharField(max_length=100, primary_key=True,unique=True)
    nomEnt = models.CharField(max_length=50)
    adresseEnt = models.CharField(max_length=255)
    cpEnt = models.IntegerField()
    villeEnt = models.CharField(max_length=100)

    def __str__(self):
        return self.nomEnt

class Theme(models.Model):
    nomTheme = models.CharField(max_length=50)
    
    def __str__(self):
        return self.nomTheme


class Responsable(models.Model):
    nomResp = models.CharField(max_length=50)
    prenomResp = models.CharField(max_length=50)
    emailResp = models.EmailField(max_length=100)
    entreprise = models.ForeignKey(Entreprise, on_delete=models.CASCADE)

    def __str__(self):
        return self.nomResp

class Tuteur(models.Model):
    nomTuteur = models.CharField(max_length=50)
    prenomTuteur = models.CharField(max_length=50)
    metierTuteur = models.CharField(max_length=50,default='')
    telTuteur = models.CharField(max_length=25)
    emailTuteur = models.EmailField(max_length=100)
    entreprise = models.ForeignKey(Entreprise, on_delete=models.CASCADE)

    def __str__(self):
        return self.nomTuteur

class Contrat(models.Model):
    type = models.CharField(max_length=50)
    description = models.TextField()
    etat = models.CharField(max_length=50)
    gratification = models.CharField(max_length=50,null=True)
    dateDeb = models.DateField()
    dateFin = models.DateField()
    estValide = models.BooleanField(default=False)
    etudiant = models.ForeignKey(ProfilEtudiant, on_delete=models.CASCADE)
    enseignant = models.ForeignKey(ProfilEnseignant, on_delete=models.CASCADE,null=True)
    tuteur = models.ForeignKey(Tuteur, on_delete=models.CASCADE,null=True)
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE)
    entreprise = models.ForeignKey(Entreprise,null=True, on_delete=models.CASCADE)
    enFrance = models.BooleanField(default=True)

    def __str__(self):
        return self.etudiant.prenomEtu+' '+self.etudiant.nomEtu

      
class Offre(models.Model):
    titre = models.CharField(max_length=100)
    description = models.TextField()
    mailRh = models.TextField()
    competences = models.TextField()
    duree = models.CharField(max_length=50)
    datePublication = models.DateField()
    entreprise = models.ForeignKey(Entreprise, on_delete=models.CASCADE)
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE)
    estPublie = models.BooleanField(default=False)

class Salle(models.Model):
    numero = models.CharField(max_length=50)

    
    def __str__(self):
        return self.numero

class Soutenance(models.Model):
    dateSoutenance = models.DateField()
    heureSoutenance = models.TimeField()
    salle = models.ForeignKey(Salle, on_delete=models.CASCADE,null=True)
    idContrat = models.ForeignKey(Contrat, on_delete=models.CASCADE,null=True)
    candide = models.ForeignKey(ProfilEnseignant, on_delete=models.CASCADE,null=True)
    estDistanciel = models.BooleanField()

class Document(models.Model):
    titre = models.CharField(max_length=255)
    fichier = models.FileField(upload_to='documents/')  # Dossier de stockage des fichiers
    contrat = models.ForeignKey('Contrat', on_delete=models.CASCADE)

    def __str__(self):
        return self.titre
    
class Evaluation(models.Model):
    contrat = models.ForeignKey('Contrat', on_delete=models.CASCADE)
    enseignant = models.ForeignKey('ProfilEnseignant', on_delete=models.CASCADE)
    note = models.DecimalField(max_digits=4, decimal_places=2)
    commentaire = models.TextField()

    def __str__(self):
        return f"Évaluation de {self.contrat.etudiant.utilisateur.username} par {self.enseignant.utilisateur.username}"
        

# INSERT INTO lesApprentiStage_offre (titre, description, competences, duree, datePublication, entreprise_id, theme_id, estPublie, date)
# VALUES ('developpement resaux', ' Venez developez des reseaux', 'apache ngnix', '3 mois', '2023-11-07', 741852, 1, 0, '2023-11-05 12:00:00');
