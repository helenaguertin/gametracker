import mysql.connector
import os

def generate_report():
    try:
        conn = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'db'),
            user=os.getenv('DB_USER', 'user'),
            password=os.getenv('DB_PASSWORD', 'password'),
            database=os.getenv('DB_NAME', 'gt_db'),
            ssl_disabled=True
        )
        cursor = conn.cursor()

        # 1. Statistiques générales
        cursor.execute("SELECT COUNT(*) FROM players")
        nb_joueurs = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM scores")
        nb_scores = cursor.fetchone()[0]

        # 2. Top 5 des meilleurs scores avec pseudos
        query_top5 = """
            SELECT p.username, s.game, s.score 
            FROM scores s 
            JOIN players p ON s.player_id = p.player_id 
            ORDER BY s.score DESC LIMIT 5
        """
        cursor.execute(query_top5)
        top5 = cursor.fetchall()

        # 3. Score moyen par jeu
        cursor.execute("SELECT game, AVG(score) FROM scores GROUP BY game")
        avg_scores = cursor.fetchall()

        # 4. Répartition par pays
        cursor.execute("SELECT country, COUNT(*) FROM players GROUP BY country")
        repartition_pays = cursor.fetchall()

        # Ecriture du fichier rapport.txt
        os.makedirs('output', exist_ok=True)
        with open('output/rapport.txt', 'w', encoding='utf-8') as f:
            f.write("=== GAMETRACKER - Rapport de synthèse ===\n")
            f.write(f"Nombre de joueurs : {nb_joueurs}\n")
            f.write(f"Nombre de scores : {nb_scores}\n\n")
            
            f.write("--- Top 5 des meilleurs scores ---\n")
            for i, (user, game, score) in enumerate(top5, 1):
                f.write(f"{i}. {user} | {game} : {score}\n")
            
            f.write("\n--- Score moyen par jeu ---\n")
            for game, avg in avg_scores:
                f.write(f"{game} : {avg:.2f}\n")

            f.write("\n--- Répartition par pays ---\n")
            for country, count in repartition_pays:
                f.write(f"{country} : {count}\n")

        print("Rapport généré avec succès dans output/rapport.txt")

    except Exception as e:
        print(f"Erreur lors de la génération du rapport : {e}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            conn.close()

if __name__ == "__main__":
    generate_report()