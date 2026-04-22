# Django-Partage_Resources_Pedagogiques
Un petit projet web en python (Django) pour la gestion de partage des ressources pedagogiques

## Prérequis
- Python 3.10+ 
- MySQL 8.0+ installé et une base de données créée
- Git cloné : `git clone https://github.com/votre-user/Django-Partage_Resources_Pedagogiques.git`

## Installation
Créez et activez un environnement virtuel, puis installez les dépendances :

**Linux/Mac :**
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Windows :**
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Configuration base de données
Dans `monprojet/settings.py`, pour les paramètres de `DATABASES` modifiez :
```python
'USER': 'postgres', # votre user
'PASSWORD': '', # votre mot de passe
```


## Lancement du projet
```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
