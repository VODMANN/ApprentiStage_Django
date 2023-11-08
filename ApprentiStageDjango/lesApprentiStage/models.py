from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _


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

class Entreprise(models.Model):
    numSiret = models.CharField(max_length=100, primary_key=True)
    nomEnt = models.CharField(max_length=50)
    adresseEnt = models.CharField(max_length=255)
    cpEnt = models.IntegerField()
    villeEnt = models.CharField(max_length=100)

class Theme(models.Model):
    nomTheme = models.CharField(max_length=50)


class Responsable(models.Model):
    nomResp = models.CharField(max_length=50)
    prenomResp = models.CharField(max_length=50)
    emailResp = models.EmailField(max_length=100)
    entreprise = models.ForeignKey(Entreprise, on_delete=models.CASCADE)

class Tuteur(models.Model):
    nomTuteur = models.CharField(max_length=50)
    prenomTuteur = models.CharField(max_length=50)
    telTuteur = models.CharField(max_length=25)
    emailTuteur = models.EmailField(max_length=100)
    entreprise = models.ForeignKey(Entreprise, on_delete=models.CASCADE)

class Contrat(models.Model):
    type = models.CharField(max_length=50)
    description = models.TextField()
    etat = models.CharField(max_length=50)
    dateDeb = models.DateField()
    dateFin = models.DateField()
    etudiant = models.ForeignKey(ProfilEtudiant, on_delete=models.CASCADE)
    enseignant = models.ForeignKey(ProfilEnseignant, on_delete=models.CASCADE)
    tuteur = models.ForeignKey(Tuteur, on_delete=models.CASCADE)
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE)

    def __str__(self):
        return self.etudiant.prenomEtu+' '+self.etudiant.nomEtu

class Offre(models.Model):
    titre = models.CharField(max_length=100)
    description = models.TextField()
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