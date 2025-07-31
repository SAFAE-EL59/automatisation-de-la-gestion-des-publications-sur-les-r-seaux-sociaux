import psycopg2
from datetime import datetime
import os

# Informations de connexion à la base de données
connection_infos = {
    "host": "localhost",
    "port": "5432",
    "dbname": "PUB_POS",
    "user": "postgres",
    "password": "592004"
}

# Limites de caractères par plateforme
limites = {
    "contenu_facebook": 2000,
    "contenu_linkedin": 3000,
    "contenu_instagram": 2200,
    "contenu_twitter": 280,
    "contenu_tiktok": 150,
}

def verification_contenu(contenus):
    erreurs = []
    for plateforme, texte in contenus.items():
        limite = limites.get(plateforme)
        if limite is None:
            continue
        if texte is None:
            erreurs.append(f"{plateforme} n'a pas de contenu défini.")
        elif len(str(texte)) > limite:
            erreurs.append(f"{plateforme} ({len(str(texte))} caractères) dépasse la limite autorisée de {limite} caractères.")
    return erreurs

def generer_sous_dictionnaires(donnees_brutes):
    sous_dictionnaires = []
    reseaux = ['facebook', 'linkedin', 'instagram', 'twitter', 'tiktok']

    for donnee in donnees_brutes:
        sous_dictionnaire = {
            'RESEAU': donnee[0].upper(),  # Réseau depuis la base
            'titre': donnee[1],
            'contenu': donnee[2],
            'image_url': donnee[3],
            'video_url': donnee[4],
            'video_duration': donnee[5],
            'date_post': donnee[6],
            'statut': donnee[7],
            'type_pub': donnee[8],
            'story_type': donnee[9] if donnee[8] == 'STORY' else None,
            'post_type': donnee[10] if donnee[8] == 'POST' else None,
            'tag_people': donnee[11]
        }
        sous_dictionnaires.append(sous_dictionnaire)

    return sous_dictionnaires

# Fonctions fictives pour les réseaux sociaux (à implémenter)
def poster_facebook(titre, contenu, image_url=None, video_url=None, tag_people=None):
    print(f"Publication sur Facebook - Titre: {titre}, Contenu: {contenu[:50]}... (Image: {image_url}, Vidéo: {video_url}, Tags: {tag_people})")
    # Implémentez ici l'appel à l'API Facebook Graph
    return True

def poster_linkedin(titre, contenu, image_url=None, video_url=None, tag_people=None):
    print(f"Publication sur LinkedIn - Titre: {titre}, Contenu: {contenu[:50]}... (Image: {image_url}, Vidéo: {video_url}, Tags: {tag_people})")
    # Implémentez ici l'appel à l'API LinkedIn
    return True

def poster_instagram(titre, contenu, image_url=None, video_url=None, tag_people=None):
    print(f"Publication sur Instagram - Titre: {titre}, Contenu: {contenu[:50]}... (Image: {image_url}, Vidéo: {video_url}, Tags: {tag_people})")
    # Implémentez ici l'appel à l'API Instagram
    return True

def poster_twitter(titre, contenu, image_url=None, video_url=None, tag_people=None):
    print(f"Publication sur Twitter - Titre: {titre}, Contenu: {contenu[:50]}... (Image: {image_url}, Vidéo: {video_url}, Tags: {tag_people})")
    # Implémentez ici l'appel à l'API Twitter
    return True

def poster_tiktok(titre, contenu, video_url=None, video_duration=None, tag_people=None):
    print(f"Publication sur TikTok - Titre: {titre}, Contenu: {contenu[:50]}... (Vidéo: {video_url}, Durée: {video_duration}, Tags: {tag_people})")
    # Implémentez ici l'appel à l'API TikTok 
    return True

def publier_sur_reseaux(sous_dicts):
    for sous_dict in sous_dicts:
        reseau = sous_dict['RESEAU'].lower()
        if reseau == 'facebook':
            poster_facebook(sous_dict['titre'], sous_dict['contenu'], sous_dict['image_url'], sous_dict['video_url'], sous_dict['tag_people'])
        elif reseau == 'linkedin':
            poster_linkedin(sous_dict['titre'], sous_dict['contenu'], sous_dict['image_url'], sous_dict['video_url'], sous_dict['tag_people'])
        elif reseau == 'instagram':
            poster_instagram(sous_dict['titre'], sous_dict['contenu'], sous_dict['image_url'], sous_dict['video_url'], sous_dict['tag_people'])
        elif reseau == 'twitter':
            poster_twitter(sous_dict['titre'], sous_dict['contenu'], sous_dict['image_url'], sous_dict['video_url'], sous_dict['tag_people'])
        elif reseau == 'tiktok':
            poster_tiktok(sous_dict['titre'], sous_dict['contenu'], sous_dict['video_url'], sous_dict['video_duration'], sous_dict['tag_people'])

# Fonction principale pour récupérer et publier
def recuperer_et_publier():
    date_actuelle = datetime.now().strftime('%Y-%m-%d')
    with psycopg2.connect(**connection_infos) as connection:
        cursor = connection.cursor()
        # Récupérer les publications prévues pour aujourd'hui avec statut 'DRAFT'
        cursor.execute("""
            SELECT reseau, titre, contenu, image_url, video_url, video_duration, date_post, statut, type_pub, story_type, post_type, tag_people
            FROM publications
            WHERE date_post = %s AND statut = 'DRAFT'
        """, (date_actuelle,))
        donnees_brutes = cursor.fetchall()

        if not donnees_brutes:
            print(f"Aucune publication trouvée pour le {date_actuelle}.")
            return

        # Générer les sous-dictionnaires
        sous_dicts = generer_sous_dictionnaires(donnees_brutes)

        # Vérifier les contenus
        contenus_a_verifier = {f'contenu_{sous["RESEAU"].lower()}': sous['contenu'] for sous in sous_dicts}
        erreurs = verification_contenu(contenus_a_verifier)
        if erreurs:
            for erreur in erreurs:
                print(erreur)
            return

        # Publier sur les réseaux sociaux
        publier_sur_reseaux(sous_dicts)

        # Mettre à jour le statut en 'PUBLISHED' après publication
        for sous_dict in sous_dicts:
            cursor.execute("""
                UPDATE publications
                SET statut = 'PUBLISHED'
                WHERE reseau = %s AND date_post = %s
            """, (sous_dict['RESEAU'], sous_dict['date_post']))
        connection.commit()
        print("Statuts mis à jour avec succès.")

if __name__ == "__main__":
    recuperer_et_publier()
