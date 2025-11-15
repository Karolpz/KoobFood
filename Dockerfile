################################################################### 
#----------------------------BUILDER------------------------------#
###################################################################

FROM python:3.13-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

EXPOSE 8000

RUN apt-get update && apt-get install -y gcc libpq-dev build-essential \
    && pip install uv \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY pyproject.toml uv.lock* ./

RUN uv sync --no-cache  

################################################################### 
#------------------------------DEV--------------------------------#
###################################################################
FROM builder AS local

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.13 /usr/local/lib/python3.13
COPY --from=builder /usr/local/bin/uv /usr/local/bin/uv
COPY . .

RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app

USER appuser

EXPOSE 8000

CMD uv run gunicorn --bind 0.0.0.0:$PORT koobfood.wsgi

###################################################################
#-----------------------------PROD--------------------------------#
###################################################################

FROM builder AS prod

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.13 /usr/local/lib/python3.13
COPY --from=builder /usr/local/bin/uv /usr/local/bin/uv
COPY . .

RUN uv sync --no-cache  --no-dev
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app

USER appuser

EXPOSE 8000 

CMD uv run gunicorn --bind 0.0.0.0:$PORT koobfood.wsgi

###################################################################
#-----------------------------TEST--------------------------------#
###################################################################
FROM builder AS test

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.13 /usr/local/lib/python3.13
COPY --from=builder /usr/local/bin/uv /usr/local/bin/uv 
COPY . .

RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

CMD ["sleep", "infinity"]

# ########LOCAL#######
# # Image Python légère avec Debian
# FROM python:3.13-slim AS local

# # Expose le port 8000 (serveur Django)
# EXPOSE 8000

# # Empêche la création de fichiers .pyc et active le log immédiat
# ENV PYTHONDONTWRITEBYTECODE=1
# ENV PYTHONUNBUFFERED=1

# # Installe les dépendances système nécessaires à psycopg2 et autres
# RUN apt-get update && apt-get install -y \
#     gcc \
#     libpq-dev \
#     build-essential \
#     && rm -rf /var/lib/apt/lists/*

# # Installe uv (le gestionnaire de paquets moderne)
# RUN pip install uv

# # Définit le dossier de travail AVANT de copier les fichiers
# WORKDIR /app

# # Copie uniquement les fichiers nécessaires à l'installation des dépendances
# COPY pyproject.toml uv.lock* ./

# # Installe les dépendances (sans créer de virtualenv)
# RUN uv sync --no-cache

# # Copie tout le code du projet
# COPY . .

# # Crée un utilisateur non-root pour des raisons de sécurité
# RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
# USER appuser

# # Commande par défaut : lance le serveur Django avec Gunicorn
# CMD ["uv", "run", "gunicorn", "--bind", "0.0.0.0:8000", "koobfood.wsgi"]



# #######PROD#######
# FROM python:3.13-slim AS prod



# ENV PYTHONDONTWRITEBYTECODE=1 \
#     PYTHONUNBUFFERED=1

# # Installe les libs système minimales
# RUN apt-get update && apt-get install -y \
#     libpq-dev \
#     && rm -rf /var/lib/apt/lists/*

# RUN pip install uv

# WORKDIR /app

# # Copie seulement les fichiers nécessaires
# COPY pyproject.toml uv.lock* ./

# # Installe uniquement les dépendances de prod
# RUN uv sync --no-cache --no-dev

# # Copie le code final
# COPY . .

# # Crée l'utilisateur
# RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
# USER appuser

# EXPOSE 8000

# # Commande finale : lance Gunicorn
# CMD ["uv", "run", "gunicorn", "--bind", "0.0.0.0:8000", "koobfood.wsgi"]