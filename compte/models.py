from django.db import models
from django.contrib.auth.models import AbstractUser,Group,Permission
from django.utils.translation import gettext_lazy as _
from django.db import models
from angaapp.models import Ville

class User(AbstractUser):
    villes = models.ManyToManyField(Ville, related_name='utilisateurs', blank=True)
    is_admin= models.BooleanField('Is admin', default=False)
    is_agent_de_liaison=models.BooleanField('Is agent de liaison', default=False)
    is_vendeur=models.BooleanField('Is vendeur(se)', default=False)