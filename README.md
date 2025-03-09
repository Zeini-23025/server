# Gestion d'Emploi du Temps - Backend

## 📌 Objectif

L'application **Gestion d'Emploi du Temps** (backend) permet de gérer les emplois du temps des enseignants, des groupes, des matières, des disponibilités des enseignants et des contraintes horaires.

## 📖 Description du Backend

### 🚀 Fonctionnalités du Backend

- **Gestion des groupes** : Ajouter et modifier des groupes et sous-groupes.
- **Gestion des matières** : Créer et associer des matières aux groupes.
- **Gestion des enseignants** : Assigner des enseignants aux matières et groupes.
- **Disponibilités des enseignants** : Planifier les créneaux disponibles des enseignants.
- **Emploi du temps** : Gérer l'affectation des enseignants et des matières aux créneaux horaires.
- **Contraintes horaires** : Définir des contraintes liées aux horaires des groupes et des matières.

### 🐳 Conteneurisation avec Docker

Le backend de l'application est conteneurisé avec **Docker** pour simplifier son déploiement et son exécution dans différents environnements.

### ⚙️ CI/CD avec GitHub Actions

Un pipeline **CI/CD** est configuré via **GitHub Actions** pour automatiser le processus de **build** et de **push** de l'image Docker vers **Docker Hub**.

## 📂 Livrables

- ✅ Code source du backend de l’application hébergé sur **GitHub**.
- ✅ **Dockerfile** pour conteneuriser l’application backend.
- ✅ Workflow GitHub Actions automatisant le build et le push de l'image Docker.
- ✅ L'URL du dépôt Docker Hub contenant l’image Docker.

## 📎 Liens Utiles

- 🔗 [Dépôt GitHub - Backend](https://github.com/Zeini-23025/server)
- 🐳 [Dépôt Docker Hub](https://hub.docker.com/r/zeini/docker-server)

## 👥 Équipe

- **Nom de l'Équipe** : NOT FOUND

## 📌 Exécution du Backend

### 🔧 Étapes pour exécuter le Backend

#### **Méthode 1 : Utilisation de Git**

Si vous souhaitez utiliser Git pour récupérer le code source et exécuter le backend directement depuis le dépôt GitHub, suivez ces étapes :

1. **Cloner le dépôt** :
    ```bash
    git clone https://github.com/Zeini-23025/server
    cd server/gestionEmploi
    ```

2. **Installer les dépendances** :
    Une fois dans le répertoire du projet, installez les dépendances nécessaires :
    ```bash
    pip install -r requirements.txt
    ```

3. **Exécuter le serveur** :
    Après avoir installé les dépendances, vous pouvez exécuter le serveur avec la commande suivante :
    ```bash
    python manage.py runserver
    ```

4. **Accéder à l’application Backend** :
    Ouvrir votre navigateur et accéder à l'API du backend via l'adresse suivante :
    - [http://localhost:8000](http://localhost:8000)

---

#### **Méthode 2 : Utilisation de Docker**

Si vous préférez utiliser Docker pour exécuter l'application sans avoir à installer les dépendances localement, suivez ces étapes :

1. **Récupérer l'image Docker depuis Docker Hub** :

    Si vous souhaitez utiliser l'image Docker pré-construite disponible sur Docker Hub, vous pouvez la tirer avec la commande suivante :
    ```bash
    docker pull zeini/docker-server:latest
    ```

2. **Exécuter le conteneur Docker** :

    Lancez le conteneur Docker en exposant le port 8000 sur votre machine :
    ```bash
    docker run -p 8000:8000 zeini/docker-server
    ```

3. **Accéder à l’application Backend** :

    Ouvrir votre navigateur et accéder à l'API du backend via l'adresse suivante :
    - [http://localhost:8000](http://localhost:8000)

---

### ⚙️ **CI/CD avec GitHub Actions**

Le backend utilise un pipeline **CI/CD** configuré via **GitHub Actions**. À chaque `push` sur la branche `main`, l'image Docker est construite et poussée vers Docker Hub. Voici un aperçu du fichier de workflow `.github/workflows/docker-publish.yml` :

