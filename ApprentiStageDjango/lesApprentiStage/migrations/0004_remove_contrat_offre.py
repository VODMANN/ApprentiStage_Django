# Generated by Django 4.2.6 on 2023-10-26 09:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lesApprentiStage', '0003_remove_etudiant_profil_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contrat',
            name='offre',
        ),
    ]
