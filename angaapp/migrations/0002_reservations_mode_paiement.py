# Generated by Django 4.2.3 on 2023-09-09 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('angaapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservations',
            name='mode_paiement',
            field=models.CharField(blank=True, choices=[('orange_money', 'Orange Money'), ('moov_money', 'Moov Money')], max_length=20),
        ),
    ]
