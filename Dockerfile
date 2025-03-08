# Étape 1 : Utiliser Python comme base
FROM python:3.10

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers du projet
COPY getionEmploi/ .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Exposer le port 8000
EXPOSE 8000

# Lancer le serveur Django
CMD ["gunicorn", "-b", "0.0.0.0:8000", "getionEmploi.wsgi:application"]
