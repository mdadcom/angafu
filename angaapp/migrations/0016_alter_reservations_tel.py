# Generated by Django 4.2.3 on 2024-02-03 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('angaapp', '0015_reservations_datedl_cnib_reservations_numero_cnib_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservations',
            name='tel',
            field=models.CharField(blank=True, max_length=80),
        ),
    ]