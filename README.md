# Mendeleïv

Une application web élégante et minimaliste qui transforme votre nom en éléments du tableau périodique.

## Description

Mendeleïv est une application web qui décompose votre nom en symboles d'éléments chimiques du tableau périodique. Avec un design minimaliste en noir et blanc, l'application offre une expérience utilisateur élégante et moderne.

## Fonctionnalités

- Conversion de noms en symboles d'éléments chimiques
- Design minimaliste noir et blanc
- Interface utilisateur intuitive et réactive
- Possibilité de télécharger les résultats en SVG
- Affichage de toutes les combinaisons possibles
- Support du défilement horizontal pour les noms longs

## Technologies utilisées

- Python avec Flask pour le backend
- HTML5, CSS3 et JavaScript pour le frontend
- SVG pour la génération des visualisations

## Installation locale

1. Clonez ce dépôt
   ```
   git clone https://github.com/votre-utilisateur/mendeleiv.git
   cd mendeleiv
   ```

2. Créez un environnement virtuel et installez les dépendances
   ```
   python -m venv venv
   source venv/bin/activate  # Sur Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Lancez l'application
   ```
   python app.py
   ```

4. Ouvrez votre navigateur à l'adresse `http://localhost:5000`

## Déploiement

L'application est prête à être déployée sur des plateformes comme Heroku, Render, ou PythonAnywhere.

```
git push heroku main
```

## Licence

Ce projet est sous licence MIT - voir le fichier LICENSE pour plus de détails. 