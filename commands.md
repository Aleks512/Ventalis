``python manage.py runserver``

#### Create le schema file pour API REST
``python manage.py spectacular --file schema.yml
``
#### Dump data from a specific app Model
``python manage.py dumpdata myapp.MyModel --indent 4 > data.json
``

``python manage.py dumpdata users.User --indent 4 > users.json
``
#### Dump data from a specific app
``python manage.py dumpdata myapp --indent 4 > myapp.json
``
``python manage.py dumpdata users --indent 4 > users.json
``

``python manage.py dumpdata users --indent 4 > category_2.json
``

``python manage.py dumpdata store.product --indent 4 > product_3.json
``

### Lister les packages installés
``pip list``
### Lister les packages installés avec leur version
``pip freeze``
#### Recuperer les dependances du projet
``pip install -r requirements.txt``

#### Mettre à jour les dependances du projet
``pip freeze > requirements.txt``

# Créez un nouvel environnement virtuel
``python -m venv venv``

### Activez l'environnement virtuel (Si PowerShell)
``venv\Scripts\Activate.ps1``
### Activez l'environnement virtuel (Si CMD)
``venv\Scripts\activate``
### Activez l'environnement virtuel (Si Bash)
``source venv/Scripts/activate``
### Installes les dépendances
``pip install -r requirements.txt``
### Créez un fichier .env à la racine du projet
``touch .env``
#COVERGE
### Install coverage
``pip install coverage``
### Generate report
``coverage run --source='.' manage.py test``
``coverage report``
### Generate html report
``coverage html``
### Generate xml report
``coverage xml``
### Generate annotate report
``coverage annotate``
### Generate erase report
``coverage erase``
### Generate run report dans le termina (list all files
``coverage run -m pytest``

### Mise à jour de coverage

`` coverage run manage.py test``
`` coverage report``
`` coverage html``

## Lancer les tests
``pytest``
##### Lancer les tests avec le coverage
``coverage run -m pytest``
##### Lancer les test avec les prints
``pytest -s``
``pytest -rP``

### Graphviz (les commandes)
#### diagram avec les relations (pointillés)
``python manage.py graph_models -a -g -o all_models.png``
``python manage.py graph_models -a -o store_models.png``
``python manage.py graph_models -e -g -o models-champs.png store``
``python manage.py graph_models -e -g -o models-champs.png app1 app2 app3 ...
``

#### diagram avec les relations et les attributs et les cardinalités et les noms des attributs et les noms des tables
``python manage.py graph_models -a --arrow-shape -g -o grouped_models3.png``
``python manage.py graph_models -a --arrow-shape normal -g -o grouped_models3.png``
``python manage.py graph_models -a --arrow-shape curve box diamond -g -o grouped_models3.png``
``python manage.py graph_models -a --arrow-shape curve box diamond inv -g -o grouped_models3.png``
``python manage.py graph_models -a --arrow-shape curve box diamond inv vee -g -o grouped_models3.png``


#### New things

``CREATE TABLE public.users_newuser (
    id bigint NOT NULL,
    password character varying(128) NOT NULL,
    last_login timestamp with time zone,
    email character varying(255) NOT NULL,
    first_name character varying(100) NOT NULL,
    last_name character varying(50) NOT NULL,
    company character varying(100) NOT NULL,
    is_active boolean NOT NULL,
    is_staff boolean NOT NULL,
    is_client boolean NOT NULL,
    is_employee boolean NOT NULL,
    is_superuser boolean NOT NULL,
    date_joined timestamp with time zone NOT NULL
);``

### Acceder aux attributs d'une istance
``david_instance = User.objects.filter(first_name="David").first()``
#### dir() renvoie une liste de tous les attributs et méthodes disponibles pour l'objet, y compris ceux hérités de ses classes parentes et ceux définis dans la classe elle-même.
``print(dir(david_instance))``
### Acceder aux dictionnaire des attributs d'une istance
#### renvoie un dictionnaire contenant les attributs spécifiques à l'instance et leurs valeurs
``david_instance.__dict__``
