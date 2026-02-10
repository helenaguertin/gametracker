#!/bin/bash
# Stopper le script à la première erreur
set -e

echo "1/4 - Attente de la base de données..."
./scripts/wait-for-db.sh

echo "2/4 - Initialisation des tables SQL..."
# Utilisation de --ssl=FALSE pour MariaDB/MySQL Client
mysql -h "$DB_HOST" -u "$DB_USER" -p"$DB_PASSWORD" "$DB_NAME" --ssl=FALSE < scripts/init-db.sql

echo "3/4 - Exécution du pipeline Python (ETL)..."
# PYTHONPATH=. permet à Python de comprendre la structure des dossiers
export PYTHONPATH=$PYTHONPATH:.
python3 src/main.py

echo "4/4 - Génération du rapport final..."
python3 src/report.py

echo "=== ÉVALUATION PRÊTE : Rapport disponible dans output/rapport.txt ==="