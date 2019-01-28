# Pre-requis

## Configurer un environnement virtuel

```bash
mkdir venv
cd venv

# Création des fichiers pour
python3 -m venv .

# Démarrer l'environnement virtuel
source bin/activate

# Quitter l'environnement virtuel
deactivate
```

## Installer Django dans l'environnement virtuel

```bash
# Depuis l'environnement virtuel
pip3 install django
```

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

```bash
# modification du fichier mysite/settings.py et INSTALLED_APPS
# Ajouter mon module et migrer les éléments (à faire au changement des modeles)
python manage.py makemigrations polls

# Migrations for 'polls':
#  polls/migrations/0001_initial.py
#    - Create model Choice
#    - Create model Question
#    - Add field question to choice

# Utilise le fichier de migration pour générer puis montrer le script à exécuter
python manage.py sqlmigrate polls 0001

```

On obtient :

BEGIN;
--
-- Create model Choice
--
CREATE TABLE "polls_choice" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "choice_text" varchar(200) NOT NULL, "votes" integer NOT NULL);
--
-- Create model Question
--
CREATE TABLE "polls_question" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "question_text" varchar(200) NOT NULL, "pub_date" datetime NOT NULL);
--
-- Add field question to choice
--
ALTER TABLE "polls_choice" RENAME TO "polls_choice__old";
CREATE TABLE "polls_choice" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "choice_text" varchar(200) NOT NULL, "votes" integer NOT NULL, "question_id" integer NOT NULL REFERENCES "polls_question" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "polls_choice" ("question_id", "votes", "choice_text", "id") SELECT NULL, "votes", "choice_text", "id" FROM "polls_choice__old";
DROP TABLE "polls_choice__old";
CREATE INDEX "polls_choice_question_id_c5b4b260" ON "polls_choice" ("question_id");
COMMIT;

### Vérification et mise à jour de la base de donnée

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

### Exemple

```python
# Il faut importer les éléments que l'on veut manipuler
from polls.models import Choice, Question

# On peut ajouter des élément (Question)
from django.utils import timezone
q = Question(question_text="What's new?", pub_date=timezone.now())

# On peut modfier les composants des élément (question_text et pub_date)
q.question_text = "What's up?"

# Il faut sauvegarder les éléments après schaque modification
q.save()
#(nécessite référence directe)

# On peut observer tout les éléments de la base de données
Question.objects.all()


# On peut filtrer les objets par ID (id)
Question.objects.filter(id=1)

# On peut filtrer les objets par texte(__startswith)
Question.objects.filter(question_text__startswith='What')

# On peut récupérer les objets par dates (_year)
from django.utils import timezone
current_year = timezone.now().year
Question.objects.get(pub_date__year=current_year)

# Faire un "get" impossible renvoie une exception
Question.objects.get(id=2)

# On peut aussi récupérer par "primary key", comme id
Question.objects.get(pk=1)


# Création et manipulation d'un objet "choice_set"
q = Question.objects.get(pk=1) #cible une question
q.choice_set.all() #montre que c'est vide
q.choice_set.create(choice_text='Not much', votes=0) #crée
q.choice_set.create(choice_text='The sky', votes=0) #crée
c = q.choice_set.create(choice_text='Just hacking again', votes=0)

c.question.question_text # montre que c'est connecté

# Nombre d'éléments
q.choice_set.count()


# L'api va aussi loin qu'il faut dans les relations avec "__"
Choice.objects.filter(question__pub_date__year=current_year)
# Liste des "Choice" => cibler les questions
# => cibler leur date de publication => cibler l'année


# Supprimer un élément (nécessite référence directe)
c = q.choice_set.create(choice_text='XD', votes=0)
c.delete()
```

## Création d'un admin

```bash
# Création d'un admin
python manage.py createsuperuser

# admin # Username
# admin@example.com # Email address
# admin # Password
# at least 8 characters
```
