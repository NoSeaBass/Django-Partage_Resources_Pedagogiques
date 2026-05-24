# Django-Partage_Resources_Pedagogiques

Projet web en Python (Django) pour la gestion et le partage de ressources pédagogiques entre enseignants et étudiants.

## Prérequis

* Python 3.10+
* PostgreSQL installé
* Git

## Installation

1. Clonez le projet :
```bash
git clone https://github.com/votre-user/Django-Partage_Resources_Pedagogiques.git
cd Django-Partage_Resources_Pedagogiques/src

```


2. Créez un environnement virtuel et installez les dépendances :
```bash
python -m venv venv
source venv/bin/activate  # Sur Windows : venv\Scripts\activate
pip install -r ../scripts/requirements.txt

```


3. Configurez l'environnement :
* Copiez le fichier de modèle : `cp .env.template .env`
* Modifiez le fichier `.env` pour y insérer vos accès à la base de données et une nouvelle `SECRET_KEY`.



## Créer une nouvelle clé secrète

Pour générer une clé unique et sécurisée pour votre installation, utilisez cette commande dans votre terminal :

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

```

## Lancement du projet

Une fois configuré dans le dossier `src/`, initialisez la base de données et lancez le serveur :

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

```

Accédez ensuite au projet à l'adresse : `http://127.0.0.1:8000/`
