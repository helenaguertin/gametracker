import pandas as pd
import os

def extract(filepath):
    """Lit un CSV et retourne un DataFrame."""
    if not os.path.exists(filepath):
        print(f"Erreur : Le fichier {filepath} n'existe pas.")
        return None
    
    df = pd.read_csv(filepath)
    print(f"Extraction réussie : {len(df)} lignes extraites de {filepath}")
    return df