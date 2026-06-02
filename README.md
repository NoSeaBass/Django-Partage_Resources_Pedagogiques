# Django-Partage_Resources_Pedagogiques

Projet web en Python (Django) pour la gestion et le partage de ressources pédagogiques entre enseignants et étudiants.

## Prérequis

* Python 3.10+
* PostgreSQL et son module python (`psycopg2-binary`)
* python-dotenv
* Pillow (pour la gestion des images)
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
* Modifiez le fichier `.env` pour y insérer vos accès à la base de données et une nouvelle `SECRET_KEY` (générée via `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`).

## Lancement du projet et Initialisation des données

Pour initialiser la base de données et charger les données de démonstration fournies :

1. Appliquez les migrations :

```bash
python manage.py migrate

```

2. Chargez les données initiales :

```bash
python manage.py loaddata initial_data.json

```

3. Créez un compte administrateur :

```bash
python manage.py createsuperuser

```

4. Lancez le serveur :

```bash
python manage.py runserver

```

Vous pouvez accéder au projet à l'adresse suivante : `http://127.0.0.1:8000/` (si vous lancez le projet en local sur votre machine).
