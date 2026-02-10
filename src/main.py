import mysql.connector
import os
import pandas as pd 
from src.extract import extract
from src.transform import transform_players, transform_scores
from src.load import load_players, load_scores

def main():
    # 1. Configuration de la connexion via variables d'environnement
    try:
        conn = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'db'),
            user=os.getenv('DB_USER', 'user'),
            password=os.getenv('DB_PASSWORD', 'password'),
            database=os.getenv('DB_NAME', 'gt_db'),
            port=int(os.getenv('DB_PORT', 3306))
        )
        print("Connexion à la base de données réussie.")
    except Exception as e:
        print(f"Erreur de connexion : {e}")
        return

    try:
        # --- ETAPE 1 : EXTRACTION ---
        print("\n--- Phase d'extraction ---")
        df_players_raw = extract('data/raw/Players.csv')
        df_scores_raw = extract('data/raw/Scores.csv')

        if df_players_raw is None or df_scores_raw is None:
            return

        # --- ETAPE 2 : TRANSFORMATION ---
        print("\n--- Phase de transformation ---")
        df_players_clean = transform_players(df_players_raw)
        
        # On récupère la liste des IDs valides pour filtrer les scores
        valid_ids = df_players_clean['player_id'].tolist()
        df_scores_clean = transform_scores(df_scores_raw, valid_ids)

        # --- ETAPE 3 : CHARGEMENT ---
        print("\n--- Phase de chargement ---")
        load_players(df_players_clean, conn)
        load_scores(df_scores_clean, conn)
        
        print("\nETL terminé avec succès !")

    finally:
        if conn.is_connected():
            conn.close()
            print("Connexion fermée.")

if __name__ == "__main__":
    main()