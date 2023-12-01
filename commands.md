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


