from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseForbidden
from django.contrib import messages
from angaapp.models import Destination
from .models import *
from django.contrib.auth.forms import UserCreationForm
from .form import *

def connecte (request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user=authenticate(request, username=username, password=password)
        if user is not None and user.is_superuser:
            login(request, user)
            return redirect('home')
        if user is not None and user.is_vendeur:
            login(request, user)
            return redirect('home')
        if user is not None and user.is_admin:
            login(request, user)
            return redirect('home')
        elif user is not None and user.is_agent_de_liaison:
            login(request, user)
            return redirect('affdesti')
        else:
            messages.success(request,("Nom utilisateur incorrect ou Mot de passe incorrect"))
            return redirect('connecte')
    else:
        return render(request,'connecte.html')
    
def deconnecte(request):
    logout(request)
    messages.success(request,("Vous êtes deconnecte"))
    return redirect('home')

def register_user(request):
    msg = None
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()

            # Récupérer les destinations sélectionnées
            destinations = form.cleaned_data.get('destinations')

            # Si des destinations ont été sélectionnées, les associer à l'utilisateur
            if destinations:
                user.destinations.set(destinations)

            msg = 'Utilisateur créé avec succès'
            return redirect('connecte')
        else:
            msg = 'Utilisateur non valide'
    else:
        form = RegisterUserForm()
    return render(request, 'register.html', {'form': form, 'msg': msg})


from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy

class ListeUtilisateurs(ListView):
    model = User
    template_name = 'liste_utilisateurs.html'
    context_object_name = 'utilisateurs'  

class AjouterUtilisateur(CreateView):
    model = User
    template_name = 'ajouter_utilisateur.html'
    fields = ['champ1', 'champ2', ...]

class EditerUtilisateur(UpdateView):
    model = User
    template_name = 'editer_utilisateur.html'
    fields = ['champ1', 'champ2', ...]

class SupprimerUtilisateur(DeleteView):
    model = User
    template_name = 'supprimer_utilisateur.html'
    success_url = reverse_lazy('liste_utilisateurs')
    
class DetailUtilisateur(DetailView):
    model = User
    template_name = 'detail_utilisateur.html'
    context_object_name = 'utilisateur'

    def get_object(self):
        # Récupère l'objet utilisateur en fonction de l'ID de l'URL
        return get_object_or_404(User, pk=self.kwargs['pk'])