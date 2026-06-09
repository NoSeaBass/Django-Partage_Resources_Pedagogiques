# UniShare – Plateforme de partage de ressources pédagogiques

UniShare est une application web développée avec Django dans le cadre du projet de fin d'année de la section Informatique de la Faculté des Sciences et Techniques (UCAD) pour l'année universitaire 2025-2026.

# Description du projet

Cette plateforme vise à faciliter la gestion et le partage de ressources pédagogiques au sein de la section informatique. Elle permet une interaction dynamique entre les différents acteurs : enseignants, enseignants responsables et étudiants .

## Prérequis

* Python 3.10+
* PostgreSQL et `psycopg2-binary`
* `python-dotenv`
* `pillow`
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
**NB :** Si vous aviez déja un environnement virtuel vous pouvez vous y connecter puis rentrer dans le dossier du projet et puis télécharger avec pip les modules présent dans `requirements.txt`.

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
