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
        fields=('societe','nom','prenom','date','time','ligne','tel','num_trans',)
        Widgets={
            'societe': forms.Select(attrs={'class': 'form-control'}),
            'nom':forms.TextInput(attrs={'class': 'form-control'}),
            'prenom':forms.TextInput(attrs={'class': 'form-control'}),
            'date':forms.DateInput(attrs={'class': 'form-control'}),
            'time': forms.TimeInput(format='%H:%M', attrs={'class': 'form-control'}),
            'ligne': forms.Select(attrs={'class': 'form-control'}),
            'tel':forms.TextInput(attrs={'class': 'form-control'}),
            'num_trans':forms.TextInput(attrs={'class': 'form-control'}),
            
            
            }
        
class SocieteForm(forms.ModelForm):
    class Meta:
        model = Societe
        fields=('ville','nom','img')
        Widgets={
            'ville':forms.Select(attrs={'class': 'form-control'}),
            'nom':forms.TextInput(attrs={'class': 'form-control'}),
            'img':forms.FileField(),
        }
        
        
class HeForm(forms.Form):
    def __init__(self, *args, **kwargs):
        heures_d = kwargs.pop('heures_d')
        super(HeForm, self).__init__(*args, **kwargs)
        self.fields['time'].queryset = heures_d

    # Vos autres champs de formulaire ici...
