# Generated by Django 4.2.7 on 2023-12-06 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lesApprentiStage', '0002_etablissement_contrat_competences_contrat_titre_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entreprise',
            name='telEnt',
            field=models.CharField(max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name='profilenseignant',
            name='telEnseignant',
            field=models.CharField(max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name='profiletudiant',
            name='telParent',
            field=models.CharField(max_length=25, null=True),
        ),
    ]
