import mysql.connector
import pandas as pd
import numpy as np # Importation de numpy pour gérer les NaN

def load_players(df, conn):
    """Insertion des joueurs dans MySQL."""
    cursor = conn.cursor()
    
    # Méthode plus robuste pour convertir les NaN/NaT en None (NULL pour MySQL)
    df_to_insert = df.replace({np.nan: None, pd.NA: None, pd.NaT: None})
    
    sql = """
    INSERT INTO players (player_id, username, email, registration_date, country, level)
    VALUES (%s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE 
    username=VALUES(username), email=VALUES(email), level=VALUES(level)
    """
    
    for _, row in df_to_insert.iterrows():
        # On s'assure que chaque valeur est un type Python natif (pas un type NumPy)
        cursor.execute(sql, tuple(row))
    
    conn.commit()
    print(f"Chargement terminé dans la table players.")

def load_scores(df, conn):
    """Insertion des scores dans MySQL."""
    cursor = conn.cursor()
    
    df_to_insert = df.replace({np.nan: None, pd.NA: None, pd.NaT: None})
    
    sql = """
    INSERT INTO scores (score_id, player_id, game, score, duration_minutes, played_at, platform)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE 
    score=VALUES(score), duration_minutes=VALUES(duration_minutes)
    """
    
    for _, row in df_to_insert.iterrows():
        # On définit explicitement les données pour être sûr de l'ordre
        data = (row.score_id, row.player_id, row.game, row.score, 
                row.duration_minutes, row.played_at, row.platform)
        cursor.execute(sql, data)
    
    conn.commit()
    print(f"Chargement terminé dans la table scores.")