# Generated by Django 5.1.4 on 2024-12-22 12:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('DPI', '0005_dpi_medecin_traitant_alter_dpi_patient_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dpi',
            name='nom',
        ),
    ]
