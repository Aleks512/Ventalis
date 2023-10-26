from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
import random
import string


class CustomUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Le champ Email doit être renseigné')
        email = self.normalize_email(email)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('first_name', extra_fields.get('first_name', ''))
        extra_fields.setdefault('last_name', extra_fields.get('last_name', ''))
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('company', 'Ventalis')
        extra_fields.setdefault('first_name', extra_fields.get('first_name', ''))
        extra_fields.setdefault('last_name', extra_fields.get('last_name', ''))
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')
        return self._create_user(email, password, **extra_fields)

    # def create_consultant(self, email, password, company, first_name, last_name, matricule, **extra_fields):
    #     extra_fields.setdefault('company', 'Ventalis')
    #     extra_fields.setdefault('matricule', generate_matricule())
    #     user = self._create_user(
    #         email=email,
    #         password=password,
    #         company=company,
    #         first_name=first_name,
    #         last_name=last_name
    #     )
    #     user.matricule = matricule
    #     user.is_consultant = True
    #     user.is_staff = True
    #     user.is_client = True
    #     user.save(using=self._db)
    #     return user


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)

    # Nouveaux champs personnalisés
    company = models.CharField(_("Société"), max_length=100)
    is_client = models.BooleanField(default=False)
    is_consultant = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS =[]

    # Utiliser le gestionnaire d'authentification personnalisé
    objects = CustomUserManager()

    # Définir les champs supplémentaires dans la classe Meta
    class Meta:
        db_table = 'custom_users'  # Nom de la table dans la base de données

    def __str__(self):
        return self.email


# Fonction pour générer un matricule aléatoire de 6 caractères
def generate_matricule():
    return ''.join(random.choices(string.digits + string.ascii_uppercase, k=6))

class Consultant(CustomUser):

    matricule = models.CharField(max_length=6, unique=True)

    def save(self, *args, **kwargs):

        if not self.matricule:
            while True:
                new_matricule = generate_matricule()
                if not Consultant.objects.filter(matricule=new_matricule).exists():
                    self.matricule = new_matricule
                    break

        if not self.email:
            base_email = f"{self.first_name.lower()}.{self.last_name.lower()}"
            email = base_email
            count = 1
            while Consultant.objects.filter(email=email).exists():
                email = f"{base_email}{count}"
                count += 1
            self.email = f"{email}@ventalis.com"

        self.is_consultant = True
        self.is_staff = True

        super().save(*args, **kwargs)

        def get_clients_count(self):
            return self.clients_set.count()


class Client(CustomUser):
    consultant_applied = models.ForeignKey('Consultant', on_delete=models.CASCADE, null=True,  related_name='clients')

    class Meta:
        db_table = "Clients"

    @staticmethod
    def create_client_with_consultant(user):
        consultants = Consultant.objects.all()
        min_clients = float('inf')
        selected_consultant = None

        for consultant in consultants:
            num_clients = consultant.clients.count()
            if num_clients < min_clients:
                min_clients = num_clients
                selected_consultant = consultant

        client = Client.objects.create(
            consultant_applied=selected_consultant,
            # Autres champs du client
        )
        return client