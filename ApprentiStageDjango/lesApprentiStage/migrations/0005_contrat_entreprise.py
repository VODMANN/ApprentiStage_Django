# Generated by Django 4.2.6 on 2023-10-27 09:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lesApprentiStage', '0004_remove_contrat_offre'),
    ]

    operations = [
        migrations.AddField(
            model_name='contrat',
            name='entreprise',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='lesApprentiStage.entreprise'),
        ),
    ]