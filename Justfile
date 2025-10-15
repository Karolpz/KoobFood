# Justfile - automatisation Django (Windows + PowerShell)
set shell := ["powershell", "-Command"]

# Lancer le serveur Django
run:
    uv run python manage.py runserver

# Créer les migrations
makemigrations:
    uv run python manage.py makemigrations

# Appliquer les migrations
migrate:
    uv run python manage.py migrate

# Créer un superutilisateur
superuser:
    uv run python manage.py createsuperuser

# Lancer les tests
test:
    uv run python manage.py test

# Lancer les tests avec coverage
coverage:
    uv run coverage run manage.py test

# Afficher le rapport de coverage
report:
    uv run coverage report

# Nettoyer les fichiers inutiles
clean:
    Get-ChildItem -Recurse -Include "__pycache__", "*.pyc" | Remove-Item -Recurse -Force

# Installation complète du projet (installe toutes les dépendances via UV)
init:
    uv add -r requirements.txt
    just makemigrations
    just migrate
    just run
