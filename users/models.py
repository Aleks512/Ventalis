from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    # Remplacer le champ de nom d'utilisateur par un champ d'adresse e-mail unique
    email = models.EmailField(unique=True)
    # Nouveaux champs personnalisés
    company = models.CharField(max_length=255)
    is_client = models.BooleanField(default=False)
    is_consultant = models.BooleanField(default=False)

    # Définir les champs supplémentaires dans la classe Meta
    class Meta:
        db_table = 'custom_user'  # Nom de la table dans la base de données

    def __str__(self):
        return self.email  # Facultatif : représentation sous forme de chaîne de caractères de l'utilisateur
