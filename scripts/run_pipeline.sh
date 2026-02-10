#!/bin/bash

echo "--- Démarrage de l'automatisation ---"

# 1. Attente de la base de données
echo "Attente de la base de données..."
# On réutilise ton script existant
./scripts/wait-for-db.sh

# 2. Initialisation des tables
echo "Initialisation des tables SQL..."
mysql -h "$DB_HOST" -u "$DB_USER" -p"$DB_PASSWORD" "$DB_NAME" < scripts/init-db.sql

# 3. Exécution du pipeline ETL Python
echo "Lancement de l'ETL..."
python3 -m src.main

# 4. Génération du rapport
echo "Génération du rapport final..."
python3 -m src.report

echo "--- Processus terminé avec succès ! ---"