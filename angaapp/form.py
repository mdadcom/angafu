from django import forms 
from .models import *
"""
class ReservationsForm(forms.ModelForm):
    class Meta:
        model = Reservations
        fields=('nom','prenom','date','time','tel','destination','num_trans')
        Widgets={
            'nom':forms.TextInput(attrs={'class': 'form-control'}),
            'prenom':forms.TextInput(attrs={'class': 'form-control'}),
            'date':forms.DateInput(attrs={'class': 'form-control'}),
            'time':forms.Select(attrs={'class': 'form-control'}),
            'destinaion':forms.Select(attrs={'class': 'form-control'}),
            'tel':forms.TextInput(attrs={'class': 'form-control'}),
            'num_trans':forms.TextInput(attrs={'class': 'form-control'}),
        }
"""
class ReservationsForm(forms.ModelForm):
    class Meta:
        model = Reservations
        fields="__all__"
        
class SocieteForm(forms.ModelForm):
    class Meta:
        model = Societe
        fields=('destination','nom','img')
        Widgets={
            'destinaion':forms.Select(attrs={'class': 'form-control'}),
            'nom':forms.TextInput(attrs={'class': 'form-control'}),
            'img':forms.FileField(),
        }