# Generated by Django 4.2.6 on 2023-10-24 15:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("lesApprentiStage", "0002_profilsecretaire_numsec"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="etudiant",
            name="profil",
        ),
        migrations.AddField(
            model_name="profilenseignant",
            name="mailEnseignant",
            field=models.EmailField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="profilenseignant",
            name="nomEnseignant",
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="profilenseignant",
            name="prenomEnseignant",
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="profiletudiant",
            name="nomEtu",
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="profiletudiant",
            name="prenomEtu",
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="contrat",
            name="enseignant",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="lesApprentiStage.profilenseignant",
            ),
        ),
        migrations.AlterField(
            model_name="contrat",
            name="etudiant",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="lesApprentiStage.profiletudiant",
            ),
        ),
        migrations.AlterField(
            model_name="profilenseignant",
            name="roleEnseignant",
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="profiletudiant",
            name="adresseEtu",
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="profiletudiant",
            name="civiliteEtu",
            field=models.CharField(max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name="profiletudiant",
            name="cpEtu",
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name="profiletudiant",
            name="promo",
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name="profiletudiant",
            name="telEtu",
            field=models.CharField(max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name="profiletudiant",
            name="villeEtu",
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.DeleteModel(
            name="Enseignant",
        ),
        migrations.DeleteModel(
            name="Etudiant",
        ),
    ]
