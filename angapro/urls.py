"""
URL configuration for angapro project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from angaapp.views import*

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('home2/', home2, name='home2'),
    path('affdestination/', affdestination, name='affdestination'),
    path('adddestination/', adddestination, name='adddestination'),
    path('addheure/', addheure, name='addheure'),
    path('affso/>', affso, name='affso'),
    path('addso/>', addso, name='addso'),
    path('affsociete/', affsociete, name='affsociete'),
    path('addsociete/', addsociete, name='addsociete'),
    path('dest/<int:destination_id>', dest, name='dest'),
    path('reserve/<int:societe_id>', reserve, name='reserve'),
    path('addreserve/<int:societe_id>', addreserve, name='addreserve'),
    path('deleteso/<int:societe_id>', deleteso, name='deleteso'),
    path('affeditso/<int:societe_id>', affeditso, name='affeditso'),
    path('updateso/<int:societe_id>', updateso, name='updateso'),
    path('deletere/<int:reservation_id>', deletere, name='deletere'),
    path('affeditre/<int:reservation_id>', affeditre, name='affeditre'),
    path('updatere/<int:reservation_id>', updatere, name='updatere'),
    path('api/societes/', SocieteListView.as_view(), name='societe-list'),
    path('api/reserve/', ReservationsListView.as_view(), name='reserve-list'),
    path('api/heur/', HeurListView.as_view(), name='heur-list'),
    path('api/destination/', DetinationListView.as_view(), name='destination-list'),
    path('affreserve/',affreserve,name='affreserve'),
    path('affconfirme/<int:reservation_id>',affconfirme,name='affconfirme'),
    path('confirme/<int:reservation_id>',confirme,name='confirme'),
    path('affdest/',affdest,name='affdest'),
    path('affdesti/',affdesti,name='affdesti'),
    path('affavalid<int:destination_id>/',aff_a_valid,name='affavalid'),
    path('affvalid/<int:reservation_id>',affvalid,name='affvalid'),
    path('rejeter/<int:reservation_id>/', rejeter, name='rejeter'),
    path('affichv/<int:confirme_id>',affichv,name='affichv'),
    path('valide/<int:confirme_id>',valide,name='valide'),
    path('affdes/<int:societe_id>',affdes,name='affdes'),
    path('affdes/<int:societe_id>',affdes,name='affdes'),
    path('success/',success,name='success'),
    path('successp/',successp,name='successp'),
    path('mon_vue/',mon_vue,name='mon_vue'),
    #path('recevoirsms/',recevoirsms,name='recevoirsms'),
    path('api/recevoirsms/', RecevoirSMS.as_view(), name='recevoirsms'),
    path('compte/', include('django.contrib.auth.urls')),
    path('compte/',include('compte.urls')),
    #path('register/user/', register_user, name='register_user'),
    #path('register/superuser/', register_superuser, name='register_superuser'),
   # path('destination/<int:destination_id>/',destination,name='destination'),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
