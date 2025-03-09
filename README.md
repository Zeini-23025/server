# Gestion d'Emploi du Temps - Backend

## 📌 Objectif

L'application **Gestion d'Emploi du Temps** (backend) permet de gérer les emplois du temps des enseignants, des groupes, des matières, des disponibilités des enseignants et des contraintes horaires.

## 📚 Description du Backend

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
- 🐳 [Dépôt Docker Hub - Backend](https://hub.docker.com/r/zeini/docker-server)
- 🔗 [Dépôt GitHub - Frontend](https://github.com/Zeini-23025/client)
- 🐳 [Dépôt Docker Hub - Frontend](https://hub.docker.com/r/zeini/docker-client)

---

### **Télécharger uniquement le Backend**

#### **Méthode 1 : Utilisation de Git**

1. **Cloner le dépôt Backend** :
    ```bash
    git clone https://github.com/Zeini-23025/server
    cd server/gestionEmploi
    ```

2. **Installer les dépendances** :
    ```bash
    pip install -r requirements.txt
    ```

3. **Exécuter le serveur** :
    ```bash
    python manage.py runserver
    ```

4. **Accéder à l’application Backend** :
    - [http://localhost:8000](http://localhost:8000)

---

#### **Méthode 2 : Utilisation de Docker**

1. **Récupérer l'image Docker depuis Docker Hub** :
    ```bash
    docker pull zeini/docker-server:latest
    ```

2. **Exécuter le conteneur Docker** :
    ```bash
    docker run -p 8000:8000 zeini/docker-server
    ```

3. **Accéder à l’application Backend** :
    - [https://docker-server-m0lg.onrender.com/](https://docker-server-m0lg.onrender.com/)

---

### **Télécharger l'ensemble du Projet (Frontend et Backend)**

#### **Méthode 1 : Utilisation de Git**

1. **Cloner le dépôt Backend avec les sous-modules** :
    ```bash
    git clone https://github.com/Zeini-23025/server.git
    cd server/

    # Récupérer le code frontend dans un sous-répertoire
    git clone https://github.com/Zeini-23025/client.git

    # Installer les dépendances backend
    cd backend/gestionEmploi
    pip install -r requirements.txt

    # Installer les dépendances frontend
    cd ../frontend
    npm install
    ```

#### **Méthode 2 : Utilisation de Docker**

1. **Tirer les images Docker pour le Backend et Frontend** :
    ```bash
    docker pull zeini/docker-server:latest
    docker pull zeini/docker-client:latest
    ```

2. **Exécuter les conteneurs Backend et Frontend** :
    ```bash
    # Exécuter le Backend
    docker run -p 8000:8000 zeini/docker-server

    # Exécuter le Frontend
    docker run -p 3000:3000 zeini/docker-client
    ```

3. **Accéder à l’application Backend et Frontend** :
    - Backend : [http://localhost:8000](http://localhost:8000)
    - Frontend : [http://localhost:3000](http://localhost:3000)

---

## 📄 License

Ce projet est sous la **MIT License** - voir le fichier [LICENSE](./LICENSE) pour plus de détails.
