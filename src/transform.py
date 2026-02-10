import pandas as pd

def transform_players(df):
    """Nettoyage des données joueurs."""
    # 1. Supprimer les doublons sur player_id
    df = df.drop_duplicates(subset=['player_id'])
    
    # 2. Nettoyer les espaces (strip) sur username
    df['username'] = df['username'].str.strip()
    
    # 3. Convertir les dates d'inscription
    df['registration_date'] = pd.to_datetime(df['registration_date'], errors='coerce')
    
    # 4. Remplacer les emails invalides (sans @) par None
    df.loc[~df['email'].str.contains('@', na=False), 'email'] = None
    
    return df

def transform_scores(df, valid_player_ids):
    """Nettoyage des données scores."""
    # 1. Supprimer les doublons sur score_id
    df = df.drop_duplicates(subset=['score_id'])
    
    # 2. Convertir les dates et types numériques
    df['played_at'] = pd.to_datetime(df['played_at'], errors='coerce')
    df['score'] = pd.to_numeric(df['score'], errors='coerce')
    df['duration_minutes'] = pd.to_numeric(df['duration_minutes'], errors='coerce')
    
    # 3. Supprimer les lignes avec score négatif ou nul
    df = df[df['score'] > 0]
    
    # 4. Supprimer les scores dont le player_id n'est pas dans valid_player_ids
    df = df[df['player_id'].isin(valid_player_ids)]
    
    return df