import mysql.connector
import os
import pandas as pd 
from extract import extract
from transform import transform_players, transform_scores
from load import load_players, load_scores

def main():
    print("--- Démarrage du Pipeline ETL ---")
    try:
        conn = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'db'),
            user=os.getenv('DB_USER', 'user'),
            password=os.getenv('DB_PASSWORD', 'password'),
            database=os.getenv('DB_NAME', 'gt_db'),
            ssl_disabled=True
        )
        
        # Chemins relatifs à la racine /app
        df_p = extract('data/raw/Players.csv')
        df_s = extract('data/raw/Scores.csv')

        if df_p is not None and df_s is not None:
            # Transformation
            df_p_clean = transform_players(df_p)
            valid_ids = df_p_clean['player_id'].tolist()
            df_s_clean = transform_scores(df_s, valid_ids)

            # Chargement (Ordre crucial pour les clés étrangères)
            load_players(df_p_clean, conn)
            load_scores(df_s_clean, conn)
            print("Pipeline ETL terminé avec succès.")
        else:
            print("Erreur : Fichiers CSV introuvables.")

    except Exception as e:
        print(f"Erreur critique : {e}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            conn.close()

if __name__ == "__main__":
    main()