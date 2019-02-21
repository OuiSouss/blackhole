# Pre-requis

## Configurer un environnement virtuel

```bash
# Création d'un répertoire pour contenir les fichiers
mkdir venv
cd venv

# Création des fichiers pour l'environnement virtuel
python3 -m venv .

# Démarrer l'environnement virtuel
source bin/activate

# Quitter l'environnement virtuel
deactivate
```

## Installer les dépendances du projet

```bash
# Depuis l'environnement virtuel
# dans le répertoire project
pip install -r requirements.txt
```

# Backend

##### Lancer l'API REST
```bash
# Depuis le répertoire "project"
cd backend/
./run.sh
```
## Lancer les unit_tests de la base de données MongoDB
```bash
cd backend/database
./script_unittest.sh
```
## Lancer la gestion de la base de données MongoDB dans la console
```bash
cd backend/database
./script.sh
```

## Tester les méthodes

```bash
# GET : Liste de toutes les routes créées
curl -i http://127.0.0.1:5000/api/subnet -X GET

# POST : Créer une route
curl -i http://127.0.0.1:5000/api/subnet -X POST -d "ip=1.13.12.1&next_hop=45.56.1.2&communities=45:4&communities=63:45"

# DELETE : Supprimer une route selon son ID
curl -i http://127.0.0.1:5000/api/subnet -X DELETE -d "id=1"
```

# Frontend

#### Important : ne pas oublier de remplacer la valeur de la clé secrète dans [secret_key.py](./frontend/secret_key.py).

## Création de l'application

```bash
# depuis le répertoire project
django-admin startproject django

# créer l'application polls depuis django
python manage.py startapp polls
```


## Lancer le site

```bash
# Depuis le répertoire django

# Lancer le site
python manage.py runserver

# Lancer avec numéro de port spécifique
python manage.py runserver 8080

# Lancer avec adresse IP et numéro de port
python manage.py runserver 10.0.0.7:8000
```

## Base de donnée

### Création et lancement

```bash
# Créer les tables de la base de données des applications par défaut
python manage.py migrate

# Lancer sqlite
sqlite3 db.sqlite3

# Montrer les migrations
.schema
```

### Gérer la base de donnée

#### Vérification et mise à jour de la base de donnée

```bash
# Vérifie s'il y a des problemes sans affecter la BD
python manage.py check

# Modifie la BD en faisant la migration, modifie tout ce qui doit être mis à jour
python manage.py migrate

# (1) Change your models (in models.py).
# (2) Run "python manage.py makemigrations" to create migrations for those changes
# (3) Run "python manage.py migrate" to apply those changes to the database.

# Donne accès à l'api BD en ligne de commandes
python manage.py shell
```

#### Création d'un admin

```bash
# Création d'un admin
python manage.py createsuperuser
```
#### Exemple de création d'un admin :
######admin  (Username)
######admin@example.com (Email address)
######admin (Password)
######Bypass password validation and create user anyway? [Y/N]

## Pages importantes :
**admin/** : interface d'administration
**dashboard/** : interface de gestion des routes

