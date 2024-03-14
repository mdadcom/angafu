from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
#from .models import CustomUser
from .models import*

admin.site.register(Pays)
admin.site.register(Ville)
admin.site.register(Quartie)
admin.site.register(Ligne)
admin.site.register(Depart)
admin.site.register(Societe)
admin.site.register(Heure_d)
admin.site.register(Reservations)
admin.site.register(SMS)
admin.site.register(Confirme)
#admin.site.register(CustomUser, UserAdmin)