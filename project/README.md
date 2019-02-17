# Important : Activer l'environnement virtual au préalable

## Installer les dépendances du projet

```bash
# Depuis le répertoire "project"
pip install -r requirements.txt
```

## Backend

##### Lancer l'API REST
```bash
# Depuis le répertoire "project"
./backend/run.sh
```

##### Run test
```bash
# Depuis le répertoire "backend"
nosetests --with-coverage tests/unittest_base.py --cover-package=backend --cover-html
```

## Frontend

##### Lancer l'application web (Django)

```bash
# Depuis le répertoire "project"

# Démarrer le serveur Django
python3 frontend/manage.py runserver

# Démarrer avec numéro de port
python manage.py runserver 8080

# Démarrer avec adresse IP et numéro de port
python manage.py runserver 10.0.0.7:8000
```
ll ne sera possible de se connecter que si un utilisateur a été créé. Pour plus d'explications : [INSTALL.md](INSTALL.md).

Le fichier [settings.py](frontend/blackhole_ui/settings.py) permet de configurer les constantes utilisées par Django.

