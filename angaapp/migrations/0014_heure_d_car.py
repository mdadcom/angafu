# Generated by Django 4.2.3 on 2024-02-01 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('angaapp', '0013_heure_d_destination'),
    ]

    operations = [
        migrations.AddField(
            model_name='heure_d',
            name='car',
            field=models.CharField(choices=[('VIP', 'VIP'), ('Standard', 'Standard')], default=1, max_length=10),
            preserve_default=False,
        ),
    ]
