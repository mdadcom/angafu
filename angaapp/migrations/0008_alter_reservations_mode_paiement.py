# Generated by Django 4.2.3 on 2024-01-05 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('angaapp', '0007_sms_alter_societe_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservations',
            name='mode_paiement',
            field=models.CharField(blank=True, choices=[('orange_money', 'Orange Money'), ('moov_money', 'Moov Money')], max_length=20, null=True),
        ),
    ]
