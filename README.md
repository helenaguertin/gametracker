# GameTracker - Pipeline ETL Automatisé

## Description
Ce projet est un pipeline de données (ETL) conteneurisé qui extrait des données de jeux vidéo (joueurs et scores), les transforme pour garantir leur qualité, et les charge dans une base de données MySQL. Un rapport final est généré automatiquement.

## Prérequis
- Docker et Docker Compose
- Python 3.11

## Structure du Projet
- `src/` : Scripts Python (Extract, Transform, Load, Report, Main)
- `scripts/` : Scripts Bash pour l'initialisation et l'automatisation
- `data/raw/` : Fichiers CSV sources
- `output/` : Contient le rapport de synthèse final

## Qualité des Données (Transformations)
Le pipeline traite les problèmes de qualité suivants :
1. **Doublons** : Suppression basée sur les identifiants uniques (`player_id`, `score_id`).
2. **Emails** : Suppression des adresses invalides (ne contenant pas de '@').
3. **Dates** : Conversion au format datetime avec gestion des erreurs.
4. **Valeurs aberrantes** : Suppression des scores négatifs ou nuls.
5. **Intégrité référentielle** : Filtrage des scores dont le joueur n'existe pas dans la base.

## Instructions de lancement
Pour exécuter l'ensemble du projet :
```bash
docker-compose up --build