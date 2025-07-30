import tweepy
from dotenv import load_dotenv
import os



load_dotenv(dotenv_path="C:/Users/imane/Desktop/PY/var_env_twitter.env")

api_key = os.getenv("TWITTER_API_KEY")
api_secret = os.getenv("TWITTER_API_SECRET")
access_token = os.getenv("TWITTER_ACCESS_TOKEN")
access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")


auth = tweepy.OAuth1UserHandler(
    api_key,
    api_secret,
    access_token,
    access_token_secret
)

api = tweepy.API(auth)
# Exemple de contenu
contenus = {
    "contenu_twitter": " Ceci est un test automatique depuis Python avec vérification."
    
    
}

# Vérification du contenu
erreurs = verification_contenu(contenus)

if erreurs:
    print(" Erreurs détectées :")
    for erreur in erreurs:
        print("-", erreur)
else:
    try:
        api.update_status(status=contenus["contenu_twitter"])
        print(" Tweet publié avec succès.")
    except Exception as e:
        print(" Erreur lors de la publication :", e)
