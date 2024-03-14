from django.shortcuts import render, redirect,get_object_or_404
#from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator
from django.db.utils import IntegrityError
from django.http import HttpResponseNotAllowed
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import*
from django.views import View
from .form import*
from django.http import HttpResponse
from rest_framework import generics
from .serializers import *
import logging
from django.conf import settings
from twilio.rest import Client
from django.db.models import Q
from django.db.models import Count
from datetime import timedelta
from django.utils import timezone
from django.db.models import Sum
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import BaseAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes, permission_classes,api_view
from rest_framework.exceptions import ParseError
from django.shortcuts import render
import requests

def is_venter(user):
    return user.role == 'venter'

def is_achat(user):
    return user.role == 'achat'


def home(request):
    return render(request, 'index.html',)

def home2(request, ):
    destination=Ville.objects.filter(nom__in=['Bobo-Dioulasso', 'Ouagadougou'])
    return render(request, 'index2.html', {'destination':destination})
def affso(request):
    
    
    form = SocieteForm(request.POST,request.FILES)

    
    return render(request, 'affso.html',{'form':form,})
def addso(request):
    
    if request.method == "POST":
        form = SocieteForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('affso')
        else:
            print(form.errors)  # Affiche les erreurs dans la console
    else:
        form = SocieteForm()

    return render(request, 'affso.html', {'form': form})


"""
def addso(request):
    if request.method=="POST":
        form=SocieteForm(request.POST)
        if form.is_valid():
            form.save()
            
        return redirect('home')
    else:
       form=SocieteForm()
        
       return redirect('home')
"""
def dest(request, destination_id):
    destination=get_object_or_404(Ville, id=destination_id)
    societe=destination.societe_set.all()
    #societe =get_object_or_404(Societe, id=societe_id)
    
    time=Heure_d.objects.all()
    destination=Ville.objects.all()
    context={
        
        'societe':societe,
        'time':time,
        'destination':destination,
        'societe':societe
    }
    return render(request, 'dest.html', context)

def affdestination(request):
    pays=Pays.objects.all()
    ville = Ville.objects.all()
    societe=Societe.objects.all()
    ligne=Ligne.objects.all()
    time=Heure_d.objects.all()
    quartie=Quartie.objects.all()
    context={'ville':ville,
             'pays':pays,
             'ligne':ligne,
             'societe':societe,
             'time':time,
             'quartie':quartie}
    return render(request, 'affdestination.html',context)

def deletepays(request, pays_id):
    pays=Pays.objects.get(id=pays_id)
    pays.delete()
    return redirect('affheuredp')

def deleteville(request, ville_id):
    ville=Ville.objects.get(id=ville_id)
    ville.delete()
    return redirect('affheuredp')


def affheuredp(request):
    pays_list=Pays.objects.all()
    ville_list = Ville.objects.all()
    societe_list = Societe.objects.all()
    time_list = Depart.objects.all()
    karti_list = Quartie.objects.all()
    
    # Pagination pour les pays
    pays_paginator = Paginator(pays_list, 10)  # 10 éléments par page
    pays_page_number = request.GET.get('pays_page')
    pays_page_obj = pays_paginator.get_page(pays_page_number)

    # Pagination pour les villes
    ville_paginator = Paginator(ville_list, 10)  # 10 éléments par page
    ville_page_number = request.GET.get('ville_page')
    ville_page_obj = ville_paginator.get_page(ville_page_number)

    # Pagination pour les heures de départ
    time_paginator = Paginator(time_list, 8)  # 10 éléments par page
    time_page_number = request.GET.get('time_page')
    time_page_obj = time_paginator.get_page(time_page_number)

    return render(request, 'affheuredp.html', {
        'pays_page':pays_page_obj,
        'ville_page': ville_page_obj,
        'time_page': time_page_obj,
        'societe_list': societe_list,
        'karti_list': karti_list
    })

def addpays(request):
    if request.method == 'POST':
        nom=request.POST.get('nom')
        Pays.objects.create(nom=nom)
    return redirect('affdestination')

def affeditpays(request, pays_id):
    pays = Pays.objects.get(id=pays_id)
    
    return render(request, 'editpays.html',{'pays':pays,})

def updatepays(request, pays_id):
    if request.method == 'POST':
        nom = request.POST.get('nom')
        pays = Pays.objects.get(id=pays_id)
        pays.nom = nom
        pays.save()
    return redirect('affheuredp')


def addville(request):
    if request.method == 'POST':
        pays_pk=request.POST.get('pays')
        pays=Pays.objects.get(pk=pays_pk)
        nom=request.POST.get('nom')
        Ville.objects.create(pays=pays,nom=nom)
    return redirect('affdestination')

def affeditville(request, ville_id):
    ville = Ville.objects.get(id=ville_id)
    pays=Pays.objects.all()
    
    return render(request, 'editville.html',{'ville':ville,'pays':pays})

def updateville(request, ville_id):
    if request.method == 'POST':
        pays_pk=request.POST.get('pays')
        pays=Pays.objects.get(pk=pays_pk)
        nom = request.POST.get('nom')
        ville = Ville.objects.get(id=ville_id)
        ville.pays=pays
        ville.nom = nom
        ville.save()
    return redirect('affheuredp')

def addkarti(request):
    if request.method == 'POST':
        ville_pk=request.POST.get('ville')
        ville=Ville.objects.get(pk=ville_pk)
        nom=request.POST.get('nom')
        Quartie.objects.create(nom=nom,ville=ville)
    return redirect('affdestination')
def addheure(request):
    if request.method == 'POST':
        time=request.POST.get('time')
        Heure_d.objects.create(time=time)
    return redirect('affdestination')
def addligne(request):
    if request.method == 'POST':
        ville_pk=request.POST.get('villedp')
        villedp=Ville.objects.get(pk=ville_pk)
        ville_pk=request.POST.get('villearv')
        villearv=Ville.objects.get(pk=ville_pk)
        Ligne.objects.create(villedp=villedp,villearv=villearv)
    return redirect('affdestination')
def deletedepart(request, time_id):
    depart=Depart.objects.get(id=time_id)
    depart.delete()
    return redirect('affheuredp')

def editedepart(request, time_id):
    time=Heure_d.objects.all()
    return render(request, 'editedepart.html',{'time':time})
def addepart(request):
    if request.method == 'POST':
        societe_pk = request.POST.get('societe')
        societe = Societe.objects.get(pk=societe_pk)
        
        ligne_pk = request.POST.get('ligne')
        ligne = Ligne.objects.get(pk=ligne_pk)
        
        quartie_pk = request.POST.get('quartie')
        quartie = Quartie.objects.get(pk=quartie_pk)
        
        car = request.POST.get('car')
        
        time_pk = request.POST.get('time')
        time = Heure_d.objects.get(pk=time_pk) if time_pk else None
        prix_str = request.POST.get('prix')
        prix = int(prix_str) + 1000 
        Depart.objects.create(societe=societe, ligne=ligne, car=car, quartie=quartie, time=time, prix=prix)
            
        return redirect('affdestination')




def get_depart_options(request):
    car = request.GET.get('car')
    ligne = request.GET.get('ligne')
    quartie = request.GET.get('quartie')
    societe_id = request.GET.get('societe_id')

    depart_par_societe = Depart.objects.filter(societe_id=societe_id)

    if quartie:
        depart_options = depart_par_societe.filter(car=car, ligne=ligne, quartie=quartie).values_list('time_id', flat=True)
        
        # Obtenir les objets Heure_d correspondant aux identifiants
        times = Heure_d.objects.filter(id__in=depart_options)

        # Créer une liste de dictionnaires avec les identifiants et les temps
        times_data = [{'id': time.id, 'time': time.time} for time in times]

        # Renvoyer les heures dans la réponse JSON
        return JsonResponse(times_data, safe=False)
    else:
        return JsonResponse([], safe=False)





def affsociete(request):
    destination = Ville.objects.all()
    return render(request, 'affsociete.html',{'destination':destination})
def addsociete(request):
    if request.method == 'POST':
        destination_pk=request.POST.get('destination')
        destination=Ville.objects.get(pk=destination_pk)
        nom=request.POST.get('nom')
        img=request.POST.get('img')
        Societe.objects.create(destination=destination,nom=nom,img=img)
    return redirect('affsociete')
def reserve(request, societe_id):
    societe = get_object_or_404(Societe, id=societe_id)
    ville = Ville.objects.all()
    societe_ville_id = societe.ville.id
    time=Heure_d.objects.all()
    quartie = Quartie.objects.filter(ville_id=societe_ville_id)
    depart_par_societe = Depart.objects.filter(societe_id=societe_id)
    ligne = Ligne.objects.filter(villedp__id=societe_ville_id)
    context = {
        'societe': societe,
        'depart_par_societe': depart_par_societe,
        'ville':ville,
        'time':time,
        'ligne': ligne,
        'quartie': quartie,
        
    }
    return render(request, 'reservation.html', context)


def deleteso(request, societe_id):
    societe=Societe.objects.get(id=societe_id)
    societe.delete()
    return redirect('home')
def affeditso(request, societe_id):
    societe=Societe.objects.get(id=societe_id)
    form=SocieteForm(request.POST or None, instance=societe)
   
    
    return render(request, 'editso.html',{'form':form,'societe':societe,})

def updateso(request, societe_id):
    societe=Societe.objects.get(id=societe_id)
    form=SocieteForm(request.POST, request.FILES,instance=societe)
    if form.is_valid():
        form.save()
    return redirect('home')
def deletere(request, reservation_id):
    reserve=Reservations.objects.get(id=reservation_id)
    reserve.delete()
    return redirect('home')
def affeditre(request, reservation_id):
    
    reservation = Reservations.objects.get(id=reservation_id)
    societe_id = reservation.societe.first().id
    societe = Societe.objects.get(id=societe_id)
    societes=Societe.objects.all()
    
    # Récupérer les lignes associées à la ville de la société
    ligne = Ligne.objects.filter(villedp_id=societe.ville_id)
    
    # Récupérer les quartiers associés à la ville de la société
    quartie = Quartie.objects.filter(ville=societe.ville)
    time=Heure_d.objects.all()
    context={
        'reservation': reservation,
        'societes': societes,
        'ligne':ligne,
        'quartie':quartie,
        'time':time}
    
    return render(request, 'editre.html',context)

def updatere(request, reservation_id):
    if request.method == 'POST':
        societe_pk = request.POST.get('societe')
        societe = Societe.objects.get(pk=societe_pk)
        tel = request.POST.get('tel')
        numero_cnib = request.POST.get('numero_cnib')
        datedl_cnib = request.POST.get('datedl_cnib')
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        date = request.POST.get('date')
        num_trans = request.POST.get('num_trans')
        car = request.POST.get('car')
        ligne_pk = request.POST.get('ligne')
        ligne = Ligne.objects.get(pk=ligne_pk)
        quartie_pk = request.POST.get('quartie')
        quartie = Quartie.objects.get(pk=quartie_pk)
        time_pk = request.POST.get('time')
        time = Heure_d.objects.get(pk=time_pk)
        
        reservation = Reservations.objects.get(id=reservation_id)
        reservation.tel = tel
        reservation.numero_cnib = numero_cnib
        reservation.datedl_cnib = datedl_cnib
        reservation.nom = nom
        reservation.prenom = prenom
        reservation.date = date
        reservation.num_trans = num_trans
        reservation.car=car
        reservation.ligne = ligne
        reservation.quartie = quartie
        reservation.time = time
        
        # Utilisez la méthode set() pour définir les valeurs du champ many-to-many societe
        reservation.societe.set([societe])
        
        reservation.save()
        return redirect('affreserve')



def addreserve(request, societe_id):
    societe = Societe.objects.get(id=societe_id)
    time = Heure_d.objects.all()
    destination = Ville.objects.all()
    depart = Depart.objects.all()
    
    if request.method == "POST":
        # Récupérer les données du formulaire
        tel = request.POST.get('tel')
        numero_cnib = request.POST.get('numero_cnib')
        datedl_cnib = request.POST.get('datedl_cnib')
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        date = request.POST.get('date')
        num_trans = request.POST.get('num_trans')
        car = request.POST.get('car')
        quartie_pk=request.POST.get('quartie')
        quartie=Quartie.objects.get(pk=quartie_pk)
        ligne_pk = request.POST.get('ligne')
        ligne = Ligne.objects.get(pk=ligne_pk)
        time_pk = request.POST.get('time')
        time = Heure_d.objects.get(pk=time_pk)

        # Créer la réservation avec les objets récupérés
        reservation = Reservations.objects.create(
            tel=tel, numero_cnib=numero_cnib, datedl_cnib=datedl_cnib, nom=nom, prenom=prenom, date=date,car=car,
            num_trans=num_trans, quartie=quartie,ligne=ligne,time=time,
        )
        
        # Ajouter la relation avec la société
        reservation.societe.add(societe)
        
        # Enregistrer la réservation
        reservation.save()
        request.session['reservation_id'] = reservation.id
        
        data = {
            'societe': {
                'pk': societe.pk,
                
            },
            'reservation': None
        }

        
        if reservation:
            data['reservation'] = {
                'pk': reservation.pk,
                'numero_cnib': reservation.numero_cnib,
                'datedl_cnib': reservation.datedl_cnib,
                'tel': reservation.tel,
                'nom': reservation.nom,
                'prenom': reservation.prenom,
                'date': reservation.date,
                'time': {'time':time.time,},
                'num_trans': reservation.num_trans,
                'ligne':{'ligne': ligne},
                
            }
        return redirect('affreserve')

class SocieteListView(generics.ListAPIView):
    queryset = Societe.objects.all()
    serializer_class = SocieteSerializer
    
class ReservationsListView(generics.ListAPIView):
    queryset = Reservations.objects.all()
    serializer_class = ReservationsSerializer

class HeurListView(generics.ListAPIView):
    queryset = Heure_d.objects.all()
    serializer_class = HeurSerializer
    
class DetinationListView(generics.ListAPIView):
    queryset = Ville.objects.all()
    serializer_class = VilleSerializer
    
def affreserve(request):
    query = request.GET.get('query') 
    if query:
        lis_reserver = Reservations.objects.filter(Q(nom__icontains=query) | Q(prenom__icontains=query) | Q(num_trans__icontains=query))
    else:
        lis_reserver = Reservations.objects.filter(val=False)
    
    # Pagination
    paginator = Paginator(lis_reserver, 5)  # 10 éléments par page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'affreserve.html', {'page_obj': page_obj, 'query': query})
def affconfirme(request, reservation_id):
    reservation = get_object_or_404(Reservations, id=reservation_id)
    return render(request,'confirme.html',{'reservation': reservation})
#def confirme(request, reservation_id):
#    if request.method == 'POST':
 #       num_trans = request.POST.get('num_trans') 
 #       trans_id = request.POST.get('trans_id')
 #       montant_paye = request.POST.get('montant_paye')
 #       reservation = Reservations.objects.get(id=reservation_id)
 #       if num_trans == reservation.num_trans or (trans_id and montant_paye == '10000'):
 #           confirme_instance = Confirme.objects.create(num_trans=num_trans,trans_id=trans_id,montant_paye=montant_paye)
 #           reservation.confirm = True
 #           reservation.save()
 #           reservation.confirme_set.add(confirme_instance)
 #       return redirect('affreserve')
 
def confirme(request, reservation_id):
    if request.method == 'POST':
        num_trans = request.POST.get('num_trans') 
        trans_id = request.POST.get('trans_id')
        montant_paye = request.POST.get('montant_paye')
        reservation = Reservations.objects.get(id=reservation_id)
        
        # Vérifier si les conditions de num_trans et montant_paye sont remplies
        montant_paye_int = int(montant_paye)  # Convertir le montant payé en entier
        if num_trans == reservation.num_trans and 3000 <= montant_paye_int <= 50000:
            confirme_instance = Confirme.objects.create(num_trans=num_trans, trans_id=trans_id, montant_paye=montant_paye)
            reservation.confirm = True
            reservation.save()
            reservation.confirme_set.add(confirme_instance)
        
        return redirect('affreserve')


def affdest(request):
    destination=Ville.objects.all()
    context={
        'destination':destination,
    }
    return render(request, 'affdest.html',context)


def affdesti(request):
    user_ville = request.user.villes.first()

    if user_ville:
        
        destination = Ville.objects.filter(nom=user_ville.nom)
        context = {
            'destination': destination,
        }
        return render(request, 'affdest.html', context)
    else:
        return HttpResponse("Vous n'avez pas de destination valide.")



def aff_a_valid(request, ville_id):
    ville=get_object_or_404(Ville, id=ville_id)
    societe=ville.societe_set.all()
    context={
        'ville':ville,
        'societe':societe
    }
    return render(request, 'affavalid.html',context)
def affvalid(request,reservation_id):
    reservation=get_object_or_404(Reservations, id=reservation_id)
    confirme_lis = reservation.confirme_set.all()
    
    return render(request, 'confirmv.html',{'confirme_lis':confirme_lis,'reservation':reservation})

#def valide(request, reservation_id):
 #   if request.method == 'POST':
 #       numticket = request.POST.get('numticket')
 #       numchaise = request.POST.get('numchaise')

  #      reservation = get_object_or_404(Reservations, id=reservation_id)

   #     try:
    #        confirme_instance = reservation.confirm.get()
     #   except Confirme.DoesNotExist:
      #      print("Aucune instance Confirme associée à cette réservation.")
       #     Valide.objects.create(confirmation=confirme_instance, numticket=numticket, numchaise=numchaise)

        # Envoi du SMS
        #account_sid = 'ACf039fa8809fc1dbe5f6a20ad139f8c20'
        #auth_token = 'a015f30efef3355999c3de439c9e9a68'
        #client = Client(account_sid, auth_token)

        #message = client.messages.create(
          #  body=f"Votre réservation a été validée avec succès. Votre numéro de ticket est {numticket} et votre numéro de chaise est {numchaise}.",
         #   from_='+14782493931',
           # to=confirme_instance.num_trans  # Utilisez confirme_instance au lieu de confirme
        #)

        #print(message.sid)  # Cela imprime l'ID du message Twilio (pour vérification)

    #return redirect('aff_a_valid')
def affichv(request, confirme_id):
    confirme=get_object_or_404(Confirme, id=confirme_id)
    
    return render(request, 'valides.html',{'confirme':confirme})

""""

def valide(request, confirme_id):
    confirme = Confirme.objects.get(id=confirme_id)
    
    if request.method == 'POST':
        numticket = request.POST.get('numticket')
        numchaise = request.POST.get('numchaise')
        
        
        account_sid = 'ACf039fa8809fc1dbe5f6a20ad139f8c20'
        auth_token = 'efeef4daa41033069d11d99c8ac8c207'
        twilio_phone_number = '+14782493931'
        
        client = Client(account_sid, auth_token)
        
        message = f'Votre ticket est validé avec succès pour la destination {", ".join(str(res.destination) for res in confirme.reservation.all())} à la gare de {", ".join(str(res.societe.first().nom) for res in confirme.reservation.all())} à {", ".join(str(res.time.time) for res in confirme.reservation.all())}. Numéro du ticket : {numticket}, chaise : {numchaise}.'
        
        
        message = client.messages.create(
            to=confirme.num_trans,
           
            from_=twilio_phone_number,
            body=message
        )
        
        valid = Valide.objects.create(numticket=numticket, numchaise=numchaise)
        valid.confirmation.add(confirme)
        valid.save()
        
        for reservation in confirme.reservation.all():
            reservation.val = True
            reservation.save()
        
        return redirect('home')
    
    return render(request, 'valide.html', {'confirme': confirme})
    
"""""

def valides(request, confirme_id):
    #confirme = Confirme.objects.get(id=confirme_id)
    confirme = get_object_or_404(Confirme, id=confirme_id)
    
    
    if request.method == 'POST':
        numticket = request.POST.get('numticket')
        numchaise = request.POST.get('numchaise')
        
        
        
        twilio_phone_number = '+14242654790'
        
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        
        message = f'Votre ticket de la compagnie {", ".join(str(res.societe.first().nom) for res in confirme.reservation.all())} est confirmé avec succès pour le trajet {", ".join(str(res.societe.first().destination.nom) for res in confirme.reservation.all())}-{", ".join(str(res.destination.nom) for res in confirme.reservation.all())} du {", ".join(res.date.strftime("%d-%m-%Y") for res in confirme.reservation.all())} à {", ".join(str(res.time.time) for res in confirme.reservation.all())}. Numéro du ticket : {numticket}, chaise : {numchaise}.'
        
        
        message = client.messages.create(
            to=confirme.num_trans,
           
            from_=twilio_phone_number,
            body=message
        )
        
        valid = Valide.objects.create(numticket=numticket, numchaise=numchaise)
        valid.confirmation.add(confirme)
        valid.save()
        
        for reservation in confirme.reservation.all():
            reservation.val = True
            reservation.save()
            
        
        
    
    return render(request, 'valides.html', {'confirme': confirme})

#def valide(request, confirme_id):
 #   confirme = Confirme.objects.get(id=confirme_id)
    
  #  if request.method == 'POST':
  #      numticket = request.POST.get('numticket')
  #      numchaise = request.POST.get('numchaise')
        
        # Paramètres nécessaires pour l'API 3mi
   #     url = 'https://www.lesmsbus.com:7170/ines.smsbus/smsbusMt'
   #     params = {
   #         'to': confirme.num_trans,  # Numéro du destinataire
   #         'text': f'Votre ticket est validé avec succès pour la destination {", ".join(str(res.destination) for res in confirme.reservation.all())} à la gare de {", ".join(str(res.societe.first().nom) for res in confirme.reservation.all())} à {", ".join(str(res.time.time) for res in confirme.reservation.all())}. Numéro du ticket : {numticket}, chaise : {numchaise}.',
   #         'username': 'seydou',
   #         'password': 'Fer60153982',
   #         'from': '226',
   #         'dlr': '1',  # Demande d'accusé de réception
   #     }
        
   #     response = requests.get(url, params=params)
        
   #     if response.status_code == 200:
   #         # Mettez à jour le champ 'val' de la réservation associée
   #         reservation = confirme.reservation
   #         reservation.val = True
   #         reservation.save()
            
   #         return redirect('home')
   #     else:
            # Gérer le cas d'échec de l'envoi du SMS
            # (par exemple, en affichant un message d'erreur)
    #        pass
        
    #return render(request, 'valide.html', {'confirme': confirme})
    """""
def valide(request, confirme_id):
    confirme = get_object_or_404(Confirme, id=confirme_id)

    if request.method == 'POST':
        numticket = request.POST.get('numticket')
        numchaise = request.POST.get('numchaise')
        url = 'https://www.lesmsbus.com:7170/ines.smsbus/smsbusMt'
        params = {
            'to': confirme.num_trans, 
            'text': f'Votre ticket est validé avec succès pour la destination {", ".join(str(res.destination) for res in confirme.reservation.all())} à la gare de {", ".join(str(res.societe.first().nom) for res in confirme.reservation.all())} à {", ".join(str(res.time.time) for res in confirme.reservation.all())}. Numéro du ticket : {numticket}, chaise : {numchaise}.',
            'username': 'seydou',
            'password': 'Fer60153982',
            'from': '226',
            'dlr': '1',
        }
        
        response = requests.get(url, params=params)
        
        if response.status_code == 200:

            valid = Valide.objects.create(numticket=numticket, numchaise=numchaise)
            valid.confirmation.add(confirme)
            valid.save()

            
            reservation = confirme.reservation.first()
            reservation.val = True
            reservation.save()

        

        return redirect('home')

    return render(request, 'valide.html', {'confirme': confirme})
"""
def rejeter(request, reservation_id):
    reservation = get_object_or_404(Reservations, id=reservation_id)
    reservation.confirme_set.all().delete()
    reservation.confirm = False
    reservation.save()
    
    # Correction de l'accès à l'attribut `ville` à partir de `societe`
    # Vérifiez d'abord si la réservation appartient à une seule société
    if reservation.societe.count() == 1:
        societe = reservation.societe.first()
        ville_id = societe.ville.id
        return redirect('affavalid', ville_id=ville_id)
    else:
        # Gérer le cas où la réservation est liée à plusieurs sociétés
        # Peut-être rediriger vers une autre vue ou afficher un message d'erreur
        return redirect('page_erreur')
def affdes(request, societe_id):
    societe = get_object_or_404(Societe, id=societe_id)
    reservations_confirmees_non_valides = societe.reservations_set.filter(confirm=True, val=False)
    return render(request, 'hu.html', {'reservations_confirmees_non_valides': reservations_confirmees_non_valides, 'societe': societe})

def destination(request, destination_id):
    try:
        societe_id = int(request.GET.get('societe_id'))  # Récupérez l'ID de la société depuis le paramètre de requête
        
        # Obtenez toutes les réservations associées à la destination spécifiée et à la société spécifiée
        reservations = Reservations.objects.filter(destination_id=destination_id, societe__id=societe_id, confirm=True)
        
        context = {
            'reservations': reservations,
        }
        
        return render(request, 'hu.html', context)
        
    except Reservations.DoesNotExist:
        return render(request, 'hu.html', {'reservations': []})


def success(request):
    # Récupérer toutes les réservations validées
    valides = Reservations.objects.filter(val=True)
    
    # Récupérer le nombre total de réservations validées
    total_reservations = valides.count()

    # Initialiser la liste pour stocker les réservations par période de 24 heures
    reservations_par_periode = []

    # Récupérer la date et l'heure actuelles
    now = timezone.now()

    # Parcourir les 7 derniers jours (vous pouvez ajuster la plage selon vos besoins)
    for i in range(7):
        debut_periode = now - timedelta(days=i+1)
        fin_periode = now - timedelta(days=i)

        # Filtrer les réservations validées pour cette période de 24 heures
        reservations_periode = valides.filter(date__range=(debut_periode, fin_periode))
        montant_periode = Confirme.objects.filter(reservation__in=reservations_periode, 
                                                  date_paiement__range=(debut_periode, fin_periode)).aggregate(total=Sum('montant_paye'))['total']
        # Ajouter les réservations et le nombre total à la liste
        reservations_par_periode.append({
            'debut_periode': debut_periode,
            'fin_periode': fin_periode,
            'reservations': reservations_periode,
            'total': reservations_periode.count(),
            'montant_total': montant_periode,
        })

    return render(request, 'success.html', {
        'valides': valides,
        
        'reservations_par_periode': reservations_par_periode,
        'total_reservations': total_reservations
    })


  
def successp(request):
    montant_total = Confirme.objects.filter(reservation__val=True).aggregate(total=Sum('montant_paye'))['total']
    valides = Reservations.objects.filter(val=True)
    valides_total = Reservations.objects.filter(val=True).values('date').annotate(total=Count('date'))
    return render(request, 'successp.html',{'valides': valides,'valides_total': valides_total,'montant_total':montant_total,})


#def register_user(request):
 #   if request.method == 'POST':
 #       form = UserCreationForm(request.POST)
 #       if form.is_valid():
   #         user = form.save()
  #          return redirect('home')  # Redirigez vers la page d'accueil ou une autre page
   # else:
   #     form = UserCreationForm()
    
    #return render(request, 'register_user.html', {'form': form})

#def register_superuser(request):
 #   if request.method == 'POST':
  #      form = UserCreationForm(request.POST)
   #     if form.is_valid():
    #        user = form.save(commit=False)
     #       user.is_staff = True
      #      user.save()
       #     return redirect('home')  # Redirigez vers la page d'accueil ou une autre page
    #else:
     #   form = UserCreationForm()
    
#    return render(request, 'register_superuser.html', {'form': form})


def mon_vue(request):
    adresse_serveur = request.get_host()
    return HttpResponse(f"L'adresse de votre serveur est : {adresse_serveur}")

"""
@csrf_exempt
def recevoirsms(request):
    if request.method == 'POST':
        corps_sms = request.POST.get('corps_sms', '')
        
        SMS.objects.create(contenu=corps_sms)
        
        return JsonResponse({'message': 'SMS enregistré avec succès'}, status=200)

    return JsonResponse({'message': 'Requête non autorisée'}, status=400)
"""

"""
@authentication_classes([])
@permission_classes([])
class RecevoirSMS(APIView):
    def post(self, request, *args, **kwargs):
        try:
            serializer = SMSSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            corps_sms = serializer.validated_data.get('corps_sms', '')
            SMS.objects.create(contenu=corps_sms)
            return Response({'message': 'SMS enregistré avec succès'}, status=status.HTTP_200_OK)
        except ParseError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
"""

#def message(request):
    # Initialiser Firebase
 #   cred = credentials.Certificate("C:\Users\Administrator\Desktop\angafu\cle\google-services.json")
  #  firebase_admin.initialize_app(cred, {'databaseURL': 'https://transreceiv-default-rtdb.firebaseio.com/'})

    # Récupérer les données depuis Firebase
   # ref = db.reference('/')
    #data = ref.get()

    # Passer les données à votre modèle ou les utiliser directement dans le contexte
    #return render(request, 'messagerie.html', {'data': data})


logger = logging.getLogger(__name__)

class AddReservationView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            # Supposons que votre requête POST contienne des champs 'speaker', 'date', 'subject', 'type', 'avatar'
            societe = request.data.get('societe')
            nom = request.data.get('nom')
            prenom = request.data.get('prenom')
            date = request.data.get('date')
            time = request.data.get('time')
            destination = request.data.get('destination')
            tel = request.data.get('tel')
            num_trans = request.data.get('num_trans')
            

            # Votre logique de traitement spécifique ici, par exemple, enregistrez l'événement dans la base de données
            reserve = Reservations.objects.create(
                societe=societe,
                nom=nom,
                prenom=prenom,
                date=date,
                time=time,
                destination=destination,
                tel=tel,
                num_trans=num_trans,
            )

            # Sérialisez l'objet Event créé
            serializer = ReservationsSerializer(reserve)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            logger.error("Une erreur s'est produite : %s" % str(e))
            return Response({"error": "Une erreur s'est produite"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    
def hview(request):
    
    heures_d = Heure_d.objects.all()
    form = HeForm(heures_d=heures_d)
    
class HeureDListCreateView(generics. ListCreateAPIView):
 queryset = Heure_d.objects.all()
 serializer_class = HeurSerializer
    

logger = logging.getLogger(__name__)

class ReceiveSMSView(APIView):
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        try:
            # Supposons que votre requête POST contienne des champs 'msg' et 'phoneNo'
            msg_body = request.data.get('msg', '')
            phone_no = request.data.get('phoneNo', '')

            # Votre logique de traitement spécifique ici, par exemple, enregistrez le message dans la base de données
            SMS.objects.create(body=msg_body, phone_number=phone_no)

            return Response({'status': 'success'})

        except Exception as e:
            logger.error("Une erreur s'est produite : %s" % str(e))
            return Response({"error": "Une erreur s'est produite"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request, *args, **kwargs):
        return Response({'status': 'error', 'message': 'Invalid request method'})


class LoadreserveView(View):
    def get(self, request):
        tel = request.GET.get('tel', None)
        reservation = get_object_or_404(Reservations, tel=tel)

        data = {
            'nom': reservation.nom,
            'prenom': reservation.prenom,
            'num_trans': reservation.num_trans,
            
        }
        
        return JsonResponse({'donneur': data})
    
    
def load_societes(request):
    ville_nom = request.GET.get('ville')
    societes = Societe.objects.filter(ville__nom=ville_nom)
    data = [{'id': societe.id, 'nom': societe.nom, 'ville': societe.ville.nom} for societe in societes]
    return JsonResponse(data, safe=False)

def load_quarties(request):
    ville = request.GET.get('ville')

    # Récupérer les quartiers correspondants à la ville spécifiée
    quarties = Quartie.objects.filter(ville__nom=ville)

    # Créer une liste des quartiers avec leurs ID et noms
    quarties_list = [{'id': quartie.id, 'nom': quartie.nom} for quartie in quarties]

    # Retourner les quartiers au format JSON
    return JsonResponse(quarties_list, safe=False)

def load_lignes(request):
    ville = request.GET.get('ville', None)
    if ville:
        lignes = Ligne.objects.filter(villedp__nom=ville).values('id', 'villearv')
        lignes_data = []
        for ligne in lignes:
            villearv_id = ligne['villearv']
            villearv = Ville.objects.get(id=villearv_id).nom
            lignes_data.append({'id': ligne['id'], 'villearv': villearv})
        return JsonResponse(lignes_data, safe=False)
    else:
        return JsonResponse([], safe=False)
    
def get_lignes_and_quarties(request):
    societe_id = request.GET.get('societe_id')
    # Récupérer les lignes associées à la société sélectionnée
    lignes = Ligne.objects.filter(societe_id=societe_id).values('id', 'villedp', 'villearv')
    # Récupérer les quartiers associés à la société sélectionnée
    quarties = Quartie.objects.filter(societe_id=societe_id).values('id', 'nom')
    return JsonResponse({'lignes': list(lignes), 'quarties': list(quarties)})

from django.http import JsonResponse
from .models import Depart, Heure_d  # Assurez-vous d'importer correctement vos modèles

def get_time(request):
    societe_id = request.GET.get('societe_id')
    
    # Obtenez les lignes, quartiers et temps en fonction de l'ID de la société sélectionnée
    depart_par_societe = Depart.objects.filter(societe_id=societe_id)
    lignes = depart_par_societe.values_list('ligne__id', 'ligne__villedp__nom', 'ligne__villearv__nom').distinct()
    quartiers = depart_par_societe.values_list('quartie__id', 'quartie__nom').distinct()
    times = depart_par_societe.values_list('time__id', 'time__time').distinct()
    
    # Construisez les données à renvoyer au format JSON
    data = {
        'lignes': [{'id': ligne_id, 'villedp': villedp, 'villearv': villearv} for ligne_id, villedp, villearv in lignes],
        'quartiers': [{'id': quartie_id, 'nom': nom} for quartie_id, nom in quartiers],
        'times': [{'id': time_id, 'time': time} for time_id, time in times]
    }
    
    return JsonResponse(data)

def confirme_reservation(request, reservation_id):
    try:
        reservation = Reservations.objects.get(id=reservation_id)
    except Reservations.DoesNotExist:
        return redirect('page_erreur')  # Gérer le cas où la réservation n'existe pas

    matching_depart = Depart.objects.filter(
        societe__in=reservation.societe.all(),  # Utilisez societe__in pour filtrer par la relation many-to-many
        ligne=reservation.ligne,
        car=reservation.car,
        quartie=reservation.quartie,
        time=reservation.time,
    ).first()

    if matching_depart:
        # Créer une instance de Confirme avec le montant approprié
        confirme_instance = Confirme.objects.create(
            num_trans=reservation.num_trans,
            montant_paye=matching_depart,  # Utiliser un champ spécifique de Depart comme montant
        )
        # Ajouter la réservation à l'instance de Confirme
        confirme_instance.reservation.add(reservation)
        reservation.confirm = True
        reservation.save()
        return redirect('affreserve')
    else:
        # Gérer le cas où aucun départ correspondant n'est trouvé ou les champs ne sont pas identiques
        return redirect('page_erreur')


def confirmt(request):
    confirmt=Confirme.objects.all()
    return render(request, 'confirmt.html', {'confirmt': confirmt})