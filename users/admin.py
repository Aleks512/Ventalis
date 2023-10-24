from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    # Vous pouvez personnaliser l'affichage des champs dans l'interface d'administration
    list_display = ('email', 'first_name', 'last_name', 'company', 'is_client', 'is_consultant')

# Enregistrez le modèle CustomUser avec la classe personnalisée CustomUserAdmin
admin.site.register(CustomUser, CustomUserAdmin)
