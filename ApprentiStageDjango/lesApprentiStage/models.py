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

    def get_user_type(self):
        return self.type_utilisateur

class ProfilEtudiant(models.Model):
    utilisateur = models.OneToOneField(Utilisateur, on_delete=models.CASCADE)
    nomEtu = models.CharField(max_length=50,null=True)
    prenomEtu = models.CharField(max_length=50,null=True)
    prenom2Etu = models.CharField(max_length=50,null=True)
    numEtu = models.CharField(max_length=35, primary_key=True)
    civiliteEtu = models.CharField(max_length=5,null=True)
    adresseEtu = models.CharField(max_length=255,null=True)
    mailEtu = models.EmailField(max_length=255,null=True)
    telEtu = models.CharField(max_length=25,null=True)
    dateNEtu = models.DateField(null=True)
    lieuNEtu = models.CharField(max_length=100,null=True)
    departementNEtu = models.CharField(max_length=100,null=True)
    nationaliteEtu = models.CharField(max_length=100,null=True)
    numDossier = models.IntegerField(null=True)
    ineEtu = models.IntegerField(null=True)
    cpEtu = models.IntegerField(null=True)
    villeEtu = models.CharField(max_length=100,null=True)
    promo = models.ForeignKey('Promo', on_delete=models.SET_NULL, null=True)
    idDepartement = models.ForeignKey('Departement', on_delete=models.CASCADE)
    adresseParent = models.CharField(max_length=255,null=True)
    cpParent = models.IntegerField(null=True)
    villeParent = models.CharField(max_length=100,null=True)
    telParent = models.CharField(max_length=25,null=True)
    mailParent = models.EmailField(max_length=100,null=True)
    remarques = models.TextField(null=True)

    def __str__(self):
        return self.utilisateur.username
    
    def get_etudiant_id_as_int(self):
        try:
            return int(self.numEtu)
        except ValueError:
            return None


class ProfilEnseignant(models.Model):
    CHEF_DEPARTEMENT = 'chef_departement'
    ENSEIGNANT_NORMAL = 'enseignant_normal'
    ENSEIGNANT_PROMO = 'enseignant_promo'
    ROLE_CHOICES = [
        (CHEF_DEPARTEMENT, 'Chef de Département'),
        (ENSEIGNANT_NORMAL, 'Enseignant Normal'),
        (ENSEIGNANT_PROMO, 'Enseignant de Promo')
    ]
    utilisateur = models.OneToOneField(Utilisateur, on_delete=models.CASCADE)
    numHarpege = models.CharField(max_length=20, primary_key=True)
    nomEnseignant = models.CharField(max_length=50, null=True)
    prenomEnseignant = models.CharField(max_length=50, null=True)
    telEnseignant = models.CharField(max_length=25, null=True)
    mailEnseignant = models.EmailField(max_length=100, null=True)
    roleEnseignant = models.CharField(max_length=50, choices=ROLE_CHOICES, null=True)
    disciplineEnseignant = models.CharField(max_length=150, null=True)

    def __str__(self):
        return self.utilisateur.username


class Promo(models.Model):
    nomPromo = models.CharField(max_length=100)
    anneeScolaire = models.CharField(max_length=100)
    departement = models.ForeignKey('Departement', on_delete=models.SET_NULL, null=True)
    parcours = models.CharField(max_length=100, null=True)
    volumeHoraire = models.FloatField(null=True)
    def __str__(self):
        return self.nomPromo


class EnseignantPromo(models.Model):
    enseignant = models.ForeignKey(ProfilEnseignant, on_delete=models.CASCADE)
    promo = models.ForeignKey(Promo, on_delete=models.CASCADE)

class ProfilSecretaire(models.Model):
    utilisateur = models.OneToOneField(Utilisateur, on_delete=models.CASCADE)
    numSec= models.CharField(max_length=20, null=True)

    def __str__(self):
        return self.utilisateur.username

class Departement(models.Model):
    nomDep = models.CharField(max_length=100)
    adresseDep = models.CharField(max_length=255)
    chef = models.ForeignKey('ProfilEnseignant', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.nomDep


class Entreprise(models.Model):
    numSiret = models.CharField(max_length=100, primary_key=True,unique=True)
    numSiren = models.CharField(max_length=100,unique=True,null=True)
    nomEnt = models.CharField(max_length=50)
    mailEnt = models.EmailField(max_length=100,null=True)
    codeNaf = models.CharField(max_length=50,null=True)
    adresseEnt = models.CharField(max_length=255)
    cpEnt = models.IntegerField()
    villeEnt = models.CharField(max_length=100)
    formeJuridique = models.CharField(max_length=100,null=True)
    telEnt = models.CharField(max_length=25,null=True)
    siteWeb = models.CharField(max_length=100,null=True)

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
    posteResp = models.CharField(max_length=50,null=True)
    entreprise = models.ForeignKey(Entreprise, on_delete=models.CASCADE)
    telResp = models.CharField(max_length=25,null=True)
    
    def __str__(self):
        return self.nomResp

class Tuteur(models.Model):
    nomTuteur = models.CharField(max_length=50)
    prenomTuteur = models.CharField(max_length=50)
    metierTuteur = models.CharField(max_length=50,default='')
    telTuteur = models.CharField(max_length=25, null=True)
    emailTuteur = models.EmailField(max_length=100)
    entreprise = models.ForeignKey(Entreprise, on_delete=models.CASCADE)

    def __str__(self):
        return self.nomTuteur

class Contrat(models.Model):
    type = models.CharField(max_length=50)
    titre = models.CharField(max_length=100,null=True)
    description = models.TextField()
    competences = models.TextField(null=True)
    etat = models.CharField(null=True,max_length=50)
    gratification = models.CharField(max_length=50,null=True)
    dateDeb = models.DateField()
    dateFin = models.DateField()
    estValide = models.BooleanField(null=True)
    etudiant = models.ForeignKey(ProfilEtudiant, on_delete=models.CASCADE)
    enseignant = models.ForeignKey(ProfilEnseignant, on_delete=models.CASCADE,null=True)
    tuteur = models.ForeignKey(Tuteur, on_delete=models.CASCADE,null=True)
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE)
    entreprise = models.ForeignKey(Entreprise,null=True, on_delete=models.CASCADE)
    enFrance = models.BooleanField(default=True)

    def annee_scolaire(self):
        if self.dateDeb.month < 9:
            annee_debut = self.dateDeb.year - 1
        else:
            annee_debut = self.dateDeb.year

        if self.dateFin.month < 9:
            annee_fin = self.dateFin.year
        else:
            annee_fin = self.dateFin.year +1

        return f"{annee_debut}-{annee_fin}"

    def __str__(self):
        return self.etudiant.prenomEtu+' '+self.etudiant.nomEtu

      
class Offre(models.Model):
    titre = models.CharField(max_length=100)
    description = models.TextField()
    mailRh = models.EmailField(max_length=100)
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
    fichier = models.FileField(upload_to='documents/')
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
        

class Etablissement(models.Model):
    nomUniversite = models.CharField(max_length=100)
    adresseUniversite = models.CharField(max_length=255)
    cpEtablissement = models.IntegerField()
    villeEtablissement = models.CharField(max_length=100)
    telEtablissement = models.CharField(max_length=25)
    mailEtablissement = models.EmailField(max_length=100)
    siretEtablissement = models.CharField(max_length=100)
    adresseEtablissement = models.CharField(max_length=255)
    nomEtablissement = models.CharField(max_length=100)
    directeurEtablissement = models.CharField(max_length=100)


    def __str__(self):
        return self.nomEtablissement
    
class NombreSoutenances(models.Model):
    enseignant = models.ForeignKey('ProfilEnseignant', on_delete=models.CASCADE)
    promo = models.ForeignKey('Promo', on_delete=models.CASCADE)
    nombreSoutenancesStage = models.PositiveIntegerField(default=0)
    nombreSoutenancesApprentissage = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('enseignant', 'promo')

    def __str__(self):
        return f"{self.enseignant} - {self.promo} : {self.nombreSoutenancesStage} soutenances en stage, {self.nombreSoutenancesApprentissage} soutenances en apprentissage"
