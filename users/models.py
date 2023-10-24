from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        extra_fields.setdefault('is_active', True)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
class CustomUser(AbstractUser):
    username = None
    # Remplacer le champ de nom d'utilisateur par un champ d'adresse e-mail unique
    email = models.EmailField(unique=True)
    # Nouveaux champs personnalisés
    company = models.CharField(_("Société"), max_length=100)
    is_client = models.BooleanField(default=False)
    is_consultant = models.BooleanField(default=False)

    # Utiliser le gestionnaire d'authentification personnalisé
    objects = CustomUserManager()

    # Définir les champs supplémentaires dans la classe Meta
    class Meta:
        db_table = 'custom_user'  # Nom de la table dans la base de données

    def __str__(self):
        return self.email  # Facultatif : représentation sous forme de chaîne de caractères de l'utilisateur
