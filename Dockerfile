# Étape 1 : Utiliser Python comme base
FROM python:3.10

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers du projet
COPY getionEmploi/ .

# Copier le fichier requirements.txt s'il est dans getionEmploi/
COPY getionEmploi/requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Exposer le port 8000
EXPOSE 8000

# Exécuter les migrations et collecter les fichiers statiques avant de lancer le serveur
CMD ["sh", "-c", "python manage.py migrate && python manage.py collectstatic --noinput && gunicorn -b 0.0.0.0:8000 getionEmploi.wsgi:application"]
