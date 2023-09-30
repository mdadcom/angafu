from django.urls import path
from compte.views import*
from . import views
urlpatterns = [
    path('connecte/',connecte, name='connecte'),
    path('deconnecte/',deconnecte, name='deconnecte'),
    path('register_user/',register_user, name='register_user'),
    path('utilisateur/', views.ListeUtilisateurs.as_view(), name='liste_utilisateurs'),
    path('utilisateur/<int:pk>/', views.DetailUtilisateur.as_view(), name='detail_utilisateur'),
    path('utilisateur/<int:pk>/editer/', views.EditerUtilisateur.as_view(), name='editer_utilisateur'),
    path('utilisateur/<int:pk>/supprimer/', views.SupprimerUtilisateur.as_view(), name='supprimer_utilisateur'),

]