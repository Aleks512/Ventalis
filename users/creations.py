from django.contrib.auth import get_user_model
from django.db import transaction
from faker import Faker
import string

fake = Faker()


@transaction.atomic
def create_consultants():
    User = get_user_model()
    for _ in range(5):
        matricule = generate_matricule()
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = fake.email()
        # Génération d'un nom d'utilisateur unique basé sur l'e-mail
        username = email.split('@')[0]
        # Création de l'utilisateur
        user = User.objects.create_consultant(
            first_name=first_name,
            last_name=last_name,
            email=email,
            company="Ventalis",
            password="azerty123",  # Mot de passe fixé à 'azerty123'
            matricule=matricule
        )

# Fonction pour générer un matricule aléatoire de 6 caractères
def generate_matricule():
    matricule = ''.join(fake.random_choices(elements=(string.digits + string.ascii_uppercase), length=6))
    return matricule

create_consultants()
