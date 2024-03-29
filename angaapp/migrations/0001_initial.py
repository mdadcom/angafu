# Generated by Django 4.2.3 on 2024-03-11 10:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Confirme',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num_trans', models.CharField(max_length=80)),
                ('trans_id', models.CharField(max_length=150)),
                ('montant_paye', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date_paiement', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Heure_d',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.TimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Ligne',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Pays',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=80)),
            ],
            options={
                'verbose_name': 'Pays',
                'verbose_name_plural': 'Pays',
            },
        ),
        migrations.CreateModel(
            name='Quartie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(blank=True, max_length=80)),
                ('date_created', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='SMS',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField()),
                ('phone_number', models.CharField(max_length=20)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Ville',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=40)),
                ('date_created', models.DateTimeField(auto_now=True)),
                ('pays', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='angaapp.pays')),
            ],
            options={
                'verbose_name': 'Ville',
                'verbose_name_plural': 'Villes',
            },
        ),
        migrations.CreateModel(
            name='Valide',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numticket', models.CharField(max_length=80)),
                ('numchaise', models.CharField(blank=True, max_length=80, null=True)),
                ('confirmation', models.ManyToManyField(to='angaapp.confirme')),
            ],
        ),
        migrations.CreateModel(
            name='Societe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(blank=True, max_length=80)),
                ('img', models.FileField(upload_to='societe_images/')),
                ('create_date', models.DateField(auto_now_add=True)),
                ('ville', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='angaapp.ville')),
            ],
            options={
                'verbose_name': 'Societe',
                'verbose_name_plural': 'Societes',
            },
        ),
        migrations.CreateModel(
            name='Reservations',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code_reservation', models.CharField(editable=False, max_length=100, unique=True)),
                ('tel', models.CharField(blank=True, max_length=80)),
                ('numero_cnib', models.CharField(blank=True, max_length=60, null=True)),
                ('datedl_cnib', models.CharField(blank=True, max_length=60, null=True)),
                ('nom', models.CharField(blank=True, max_length=80)),
                ('prenom', models.CharField(blank=True, max_length=80)),
                ('date', models.DateField()),
                ('mode_paiement', models.CharField(blank=True, choices=[('orange_money', 'Orange Money'), ('moov_money', 'Moov Money')], max_length=20, null=True)),
                ('num_trans', models.CharField(blank=True, max_length=80)),
                ('confirm', models.BooleanField(default=False)),
                ('val', models.BooleanField(default=False)),
                ('create_date', models.DateField(auto_now_add=True)),
                ('ligne', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='angaapp.ligne')),
                ('quartie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='angaapp.quartie')),
                ('societe', models.ManyToManyField(to='angaapp.societe')),
                ('time', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='angaapp.heure_d')),
            ],
            options={
                'verbose_name': 'Reservation',
                'verbose_name_plural': 'Reservations',
                'db_table': 'reservations',
                'ordering': ['-create_date'],
            },
        ),
        migrations.AddField(
            model_name='quartie',
            name='ville',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='angaapp.ville'),
        ),
        migrations.AddField(
            model_name='ligne',
            name='villearv',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lignes_arv', to='angaapp.ville'),
        ),
        migrations.AddField(
            model_name='ligne',
            name='villedp',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lignes_dp', to='angaapp.ville'),
        ),
        migrations.CreateModel(
            name='Depart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('car', models.CharField(choices=[('VIP', 'VIP'), ('Standard', 'Standard')], max_length=10)),
                ('prix', models.DecimalField(decimal_places=2, max_digits=10)),
                ('create_date', models.DateField(auto_now_add=True)),
                ('ligne', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='angaapp.ligne')),
                ('quartie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='angaapp.quartie')),
                ('societe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='angaapp.societe')),
                ('time', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='angaapp.heure_d')),
            ],
        ),
        migrations.AddField(
            model_name='confirme',
            name='reservation',
            field=models.ManyToManyField(to='angaapp.reservations'),
        ),
    ]
