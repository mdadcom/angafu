# Generated by Django 4.2.3 on 2024-01-08 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('angaapp', '0008_alter_reservations_mode_paiement'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sms',
            old_name='contenu',
            new_name='body',
        ),
        migrations.RenameField(
            model_name='sms',
            old_name='date_reception',
            new_name='timestamp',
        ),
        migrations.AddField(
            model_name='sms',
            name='phone_number',
            field=models.CharField(default=1, max_length=20),
            preserve_default=False,
        ),
    ]