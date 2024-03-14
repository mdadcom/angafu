#from django.contrib.auth.models import AbstractUser, BaseUserManager
#from django.contrib.auth.models import Group,Permission
#from django.utils.translation import gettext_lazy as _
#from django.core import validators
from django.db import models
import datetime
from twilio.rest import Client

class Pays (models.Model):
    nom=models.CharField(max_length=80)
    class Meta:
        verbose_name=("Pays")
        verbose_name_plural=("Pays")
    def __str__(self):
        return self.nom

class Ville(models.Model):
    pays=models.ForeignKey(Pays, on_delete=models.CASCADE)
    nom=models.CharField(max_length=40)
    date_created= models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name = ("Ville")
        verbose_name_plural = ("Villes")
    def __str__(self):
        return self.nom
    
class Quartie(models.Model):
    ville=models.ForeignKey(Ville, on_delete=models.CASCADE)
    nom=models.CharField(max_length=80, blank=True)
    date_created=models.DateField(auto_now_add=True)
    def __str__(self):
        return self.nom


    
class Ligne(models.Model):
    villedp=models.ForeignKey(Ville, related_name='lignes_dp', on_delete=models.CASCADE)
    villearv=models.ForeignKey(Ville, related_name='lignes_arv', on_delete=models.CASCADE)
    date_created=models.DateField(auto_now_add=True)
    def __str__(self):
        return f"{self.villedp.nom} - {self.villearv.nom}"
    
    
class Societe(models.Model):
    ville=models.ForeignKey(Ville, on_delete=models.CASCADE)
    nom=models.CharField(max_length=80, blank=True)
    img = models.FileField(upload_to='societe_images/')

    create_date=models.DateField(auto_now_add=True)
    class Meta:
        verbose_name=('Societe')
        verbose_name_plural=('Societes')
    def __str__(self):
        return self.nom
    
    
class Heure_d(models.Model):
    
    time = models.TimeField()

    def __str__(self):
        return self.time.strftime('%H:%M:%S')  # Formatage de l'heure pour l'affichage

    
class Depart(models.Model):
    societe = models.ForeignKey(Societe, on_delete=models.CASCADE)
    ligne = models.ForeignKey(Ligne, on_delete=models.CASCADE)
    quartie = models.ForeignKey(Quartie, on_delete=models.CASCADE)
    car = models.CharField(max_length=10, choices=[('VIP', 'VIP'), ('Standard', 'Standard')])
    time = models.ForeignKey(Heure_d, on_delete=models.CASCADE)
    prix = models.DecimalField(max_digits=10, decimal_places=2)  # Champ prix
    create_date= models.DateField(auto_now_add=True)
    def __str__(self):
        return f"{self.ligne}"
    
class Reservations(models.Model):
    MODE_PAIEMENT_CHOICES = (
        ('orange_money', 'Orange Money'),
        ('moov_money', 'Moov Money'),
    )
    
    code_reservation = models.CharField(max_length=100, unique=True, editable=False)
    societe=models.ManyToManyField(Societe,)
    tel=models.CharField(max_length=80, blank=True)
    numero_cnib=models.CharField(max_length=60, null=True,blank=True)
    datedl_cnib=models.CharField(max_length=60, null=True,blank=True)
    nom=models.CharField(max_length=80, blank=True)
    prenom=models.CharField(max_length=80, blank=True)
    date=models.DateField()
    time=models.ForeignKey(Heure_d, on_delete=models.CASCADE)
    ligne=models.ForeignKey(Ligne, on_delete=models.CASCADE)
    car = models.CharField(max_length=10, choices=[('VIP', 'VIP'), ('Standard', 'Standard')])
    quartie=models.ForeignKey(Quartie, on_delete=models.CASCADE)
    mode_paiement = models.CharField(max_length=20, choices=MODE_PAIEMENT_CHOICES,null=True, blank=True)
    num_trans=models.CharField(max_length=80, blank=True)
    confirm = models.BooleanField(default=False)
    val = models.BooleanField(default=False)
    create_date= models.DateField(auto_now_add=True)
    
    class Meta:
            
            verbose_name =('Reservation')
            verbose_name_plural=('Reservations')
            db_table='reservations'
            ordering = ['-create_date']
    def generate_code(self):
        date_part = datetime.datetime.now().strftime("%d%m%Y")
        last_reservation = Reservations.objects.order_by('-id').first()
        if last_reservation:
            last_code_reservation = int(last_reservation.code_reservation[-1])
            new_code_reservation = last_code_reservation + 1
        else:
            new_code_reservation = 1
        code_reservation = f"{self.prenom[:1]}{self.nom[:1]}{date_part}{str(new_code_reservation).zfill(4)}"
        return code_reservation
    def save(self, *args, **kwargs):
        if not self.code_reservation:
            self.code_reservation = self.generate_code()
        super().save(*args, **kwargs)
    def __str__(self):
        return f"{self.nom} {self.prenom}"
class Confirme(models.Model):
    reservation = models.ManyToManyField(Reservations,)
    num_trans=models.CharField(max_length=80,)
    trans_id= models.CharField(max_length=150,)
    montant_paye = models.ForeignKey(Depart, on_delete=models.CASCADE)
    date_paiement = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.num_trans
class Valide(models.Model):
    confirmation = models.ManyToManyField(Confirme,)
    numticket = models.CharField(max_length=80,)
    numchaise = models.CharField(max_length=80, null=True, blank=True)
    def __str__(self):
        return self.numticket
    
from django.db import models

class SMS(models.Model):
    body = models.TextField()
    phone_number = models.CharField(max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True)
