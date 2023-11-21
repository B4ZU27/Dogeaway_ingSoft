# Generated by Django 4.2.6 on 2023-11-19 23:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "main_app",
            "0002_remove_mascota_matches_remove_preferencias_mascota_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="usuario",
            name="fotografia_identificacion",
            field=models.ImageField(
                blank=True, null=True, upload_to="identificaciones/"
            ),
        ),
        migrations.AddField(
            model_name="usuario",
            name="verificado",
            field=models.BooleanField(default=False),
        ),
    ]