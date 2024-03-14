from rest_framework import serializers
from .models import *

class SocieteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Societe
        fields = '__all__'

class ReservationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservations
        fields= '__all__'
        
class HeurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Heure_d
        fields= '__all__'
        
class VilleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ville
        fields= '__all__'
        
class SMSSerializer(serializers.ModelSerializer):
    class Meta:
        model = SMS
        fields= '__all__'