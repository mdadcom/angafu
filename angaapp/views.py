from django.shortcuts import render, redirect,get_object_or_404
#from django.contrib.auth.decorators import user_passes_test
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import*
from .form import*
from django.http import HttpResponse
from rest_framework import generics
from .serializers import *
import logging
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
    destination=Destination.objects.filter(nom__in=['Bobo-Dioulasso', 'Ouagadougou'])
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
    destination=get_object_or_404(Destination, id=destination_id)
    societe=destination.societe_set.all()
    #societe =get_object_or_404(Societe, id=societe_id)
    
    time=Heure_d.objects.all()
    destination=Destination.objects.all()
    context={
        
        'societe':societe,
        'time':time,
        'destination':destination,
        'societe':societe
    }
    return render(request, 'dest.html', context)

def affdestination(request):
    destination = Destination.objects.all()
    return render(request, 'affdestination.html',)
def adddestination(request):
    if request.method == 'POST':
        nom=request.POST.get('nom')
        Destination.objects.create(nom=nom)
    return redirect('affdestination')
def addheure(request):
    if request.method == 'POST':
        time=request.POST.get('time')
        Heure_d.objects.create(time=time)
    return redirect('affdestination')
def affsociete(request):
    destination = Destination.objects.all()
    return render(request, 'affsociete.html',{'destination':destination})
def addsociete(request):
    if request.method == 'POST':
        destination_pk=request.POST.get('destination')
        destination=Destination.objects.get(pk=destination_pk)
        nom=request.POST.get('nom')
        img=request.POST.get('img')
        Societe.objects.create(destination=destination,nom=nom,img=img)
    return redirect('affsociete')
def reserve(request, societe_id):
    
    societe =get_object_or_404(Societe, id=societe_id)
    societe_destination_id = societe.destination.id
    time=Heure_d.objects.all()
    destination=Destination.objects.exclude(id=societe_destination_id)
    context={
        
        'societe':societe,
        'time':time,
        'destination':destination,
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
    form = ReservationsForm(request.POST or None, instance=reservation)
    
    return render(request, 'editre.html', {'form': form, 'reservation': reservation})

def updatere(request, reservation_id):
    reservation= Reservations.objects.get(id=reservation_id)
    form = ReservationsForm(request.POST, instance=reservation)
    if form.is_valid():
        form.save()
        return redirect('affreserve')


def addreserve(request, societe_id):
    societe = Societe.objects.get(id=societe_id)
    time=Heure_d.objects.all()
    destination=Destination.objects.all()
    if request.method=="POST":
        societe_nom = [x.nom for x in Societe.objects.all()]
        societe_ids=[Societe.objects.get(id=societe_id)]
        
        nom = request.POST.get('nom') 
        prenom = request.POST.get('prenom')
        date=request.POST.get('date')
        time_pk=request.POST.get('time')
        time=Heure_d.objects.get(pk=time_pk)
        tel = request.POST.get('tel')
        num_trans=request.POST.get('num_trans')
        destination_pk=request.POST.get('destination')
        destination=Destination.objects.get(pk=destination_pk)
        
        reservation = Reservations.objects.create(nom=nom, prenom=prenom,date=date,
                                                        time=time, tel=tel, num_trans=num_trans ,destination=destination)
        
        reservation.societe.add(Societe.objects.get(id=societe_id))
        reservation.save()
        request.session['reservation_id'] = reservation.id
        return redirect('affreserve')
    return render(request, 'reservation.html',{'societe':societe})

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
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer
    
def affreserve(request):
    query = request.GET.get('query') 
    if query:
        lis_reserver = Reservations.objects.filter(Q(nom__icontains=query) | Q(prenom__icontains=query) | Q(num_trans__icontains=query))
    else:
        lis_reserver = Reservations.objects.filter(val=False)
    return render(request, 'affreserve.html', {'lis_reserver': lis_reserver, 'query': query})
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
        if num_trans == reservation.num_trans and montant_paye in ['7000','7500','9000','8000','10000', '15000', '20000']:
            confirme_instance = Confirme.objects.create(num_trans=num_trans, trans_id=trans_id, montant_paye=montant_paye)
            reservation.confirm = True
            reservation.save()
            reservation.confirme_set.add(confirme_instance)
        
        return redirect('affreserve')


def affdest(request):
    destination=Destination.objects.all()
    context={
        'destination':destination,
    }
    return render(request, 'affdest.html',context)


def affdesti(request):
    user_destination = request.user.destinations.first()

    if user_destination:
        
        destination = Destination.objects.filter(nom=user_destination.nom)
        context = {
            'destination': destination,
        }
        return render(request, 'affdest.html', context)
    else:
        return HttpResponse("Vous n'avez pas de destination valide.")



def aff_a_valid(request, destination_id):
    destination=get_object_or_404(Destination, id=destination_id)
    societe=destination.societe_set.all()
    context={
        'destination':destination,
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
        
        
        account_sid = 'AC2727fa292b9137861bd7b1f2b9437a20'
        auth_token = '4585cd64034843697f70baa31aea8e9d'
        twilio_phone_number = '+14242654790'
        
        client = Client(account_sid, auth_token)
        
        message = f'Votre ticket de la compagnie {", ".join(str(res.societe.first().nom) for res in confirme.reservation.all())} est confirmé avec succès pour le trajet {", ".join(str(res.societe.first().destination.nom) for res in confirme.reservation.all())}-{", ".join(str(res.destination.nom) for res in confirme.reservation.all())} le {", ".join(res.date.strftime("%d-%m-%Y") for res in confirme.reservation.all())} à {", ".join(str(res.time.time) for res in confirme.reservation.all())}. Numéro du ticket : {numticket}, chaise : {numchaise}.'
        
        
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
    
    destination_id = reservation.destination.id
    
    return redirect('affavalid', destination_id=destination_id)
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

