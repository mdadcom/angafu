
""""
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from .models import CustomUser, Role

from django import forms

class RegisterUserForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    destination = forms.ModelChoiceField(queryset=Destination.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2','destination')

    def __init__(self, *args, **kwargs):
        super(RegisterUserForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'

        
        
from django import forms

class RoleAssignmentForm(forms.Form):
    user = forms.ModelChoiceField(queryset=CustomUser.objects.all())
    role = forms.ModelChoiceField(queryset=Role.objects.all())
"""
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import User
from angaapp.models import Destination
"""
class LoginForm(froms.Form):
    user
    """
    
class RegisterUserForm(UserCreationForm):
    username=forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1=forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2=forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email=forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    destinations = forms.ModelMultipleChoiceField(queryset=Destination.objects.all(), widget=forms.SelectMultiple(attrs={'class': 'form-control'}), required=False)
    
    class Meta:
        model= User
        fields= ('username','email','password1','password2','destinations','is_admin','is_agent_de_liaison','is_vendeur')