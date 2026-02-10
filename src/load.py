import mysql.connector

def load_players(df, conn):
    """Insertion des joueurs dans MySQL."""
    cursor = conn.cursor()
    # Conversion des NaN de pandas en None pour MySQL
    df = df.where(pd.notnull(df), None)
    
    sql = """
    INSERT INTO players (player_id, username, email, registration_date, country, level)
    VALUES (%s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE 
    username=VALUES(username), email=VALUES(email), level=VALUES(level)
    """
    
    for _, row in df.iterrows():
        cursor.execute(sql, tuple(row))
    
    conn.commit()
    print(f"{cursor.rowcount} lignes traitées dans la table players.")

def load_scores(df, conn):
    """Insertion des scores dans MySQL."""
    cursor = conn.cursor()
    df = df.where(pd.notnull(df), None)
    
    sql = """
    INSERT INTO scores (score_id, player_id, game, score, duration_minutes, played_at, platform)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE 
    score=VALUES(score), duration_minutes=VALUES(duration_minutes)
    """
    
    for _, row in df.iterrows():
        # On ne prend que les colonnes correspondant à la table scores
        data = (row.score_id, row.player_id, row.game, row.score, 
                row.duration_minutes, row.played_at, row.platform)
        cursor.execute(sql, data)
    
    conn.commit()
    print(f"{cursor.rowcount} lignes traitées dans la table scores.")
    