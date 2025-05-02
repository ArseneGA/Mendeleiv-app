# Guide de déploiement - Mendeleïv

Ce guide vous explique comment déployer l'application Mendeleïv sur différentes plateformes.

## 1. Render (Recommandé - Simple et gratuit)

Render est l'une des options les plus simples pour déployer une application Flask.

1. Créez un compte sur [Render.com](https://render.com).
2. Depuis le dashboard, cliquez sur "New +" puis "Web Service".
3. Connectez votre dépôt GitHub/GitLab ou utilisez l'option "Public Git repository".
4. Configurez les paramètres suivants :
   - **Name**: mendeleiv (ou le nom que vous souhaitez)
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Plan**: Free

Render détectera automatiquement qu'il s'agit d'une application Python et s'occupera du reste !

## 2. PythonAnywhere (Spécialisé Python)

PythonAnywhere est idéal pour les applications Python et dispose d'un plan gratuit généreux.

1. Créez un compte sur [PythonAnywhere.com](https://www.pythonanywhere.com).
2. Dans le dashboard, allez à l'onglet "Web" et cliquez sur "Add a new web app".
3. Choisissez "Flask" comme framework.
4. Importez votre code via GitHub ou en téléchargeant les fichiers.
5. Configurez le fichier WSGI pour pointer vers votre application Flask.
6. Dans la section "Web", configurez:
   - Source code: `/home/votreusername/mendeleiv`
   - Working directory: `/home/votreusername/mendeleiv`
   - WSGI configuration file: utilisez le fichier généré automatiquement

## 3. Heroku (Plus de fonctionnalités)

Heroku propose une excellente intégration avec les applications Flask.

1. Créez un compte sur [Heroku.com](https://www.heroku.com).
2. Installez l'[Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli).
3. Ouvrez un terminal et connectez-vous:
   ```
   heroku login
   ```
4. Dans le dossier de votre projet, initialisez un dépôt git s'il n'existe pas déjà:
   ```
   git init
   git add .
   git commit -m "Initial commit"
   ```
5. Créez une application Heroku:
   ```
   heroku create
   ```
6. Déployez votre code:
   ```
   git push heroku main
   ```
7. Ouvrez votre application:
   ```
   heroku open
   ```

## 4. Railway.app (Moderne et intuitif)

Railway est une plateforme moderne avec une excellente expérience développeur.

1. Créez un compte sur [Railway.app](https://railway.app).
2. Créez un nouveau projet et choisissez "Deploy from GitHub repo".
3. Sélectionnez votre dépôt GitHub contenant Mendeleïv.
4. Railway détectera automatiquement que c'est un projet Python.
5. Ajoutez les variables d'environnement nécessaires.
6. Cliquez sur "Deploy" et Railway s'occupera du reste.

## Notes importantes

- Tous ces services proposent des plans gratuits suffisants pour une utilisation personnelle ou pour des projets avec un trafic modéré.
- Assurez-vous que votre fichier `requirements.txt` est à jour avant le déploiement.
- Le fichier `Procfile` est nécessaire pour Heroku et Railway mais pas pour Render ou PythonAnywhere.
- Pour les déploiements avec un nom de domaine personnalisé, vous devrez souscrire à un plan payant sur la plupart des plateformes.

## Besoin d'aide?

Si vous rencontrez des problèmes lors du déploiement, n'hésitez pas à:
- Consulter la documentation spécifique à la plateforme
- Vérifier les logs d'erreur sur la plateforme
- Poser vos questions sur des forums comme Stack Overflow 