import os
import pickle
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import googleapiclient.http

SCOPES = ["https://www.googleapis.com/auth/youtube"]

def authenticate_youtube():
    client_secrets_file = "C:/Users/imane/Downloads/client1.json" #a installer depuis api youtube
    token_file = "token.json"  # Fichier pour stocker les credentials persistants

    if not os.path.exists(client_secrets_file):
        raise Exception(f"Le fichier client_secrets {client_secrets_file} n'existe pas.")

    # Charger les credentials persistants s'ils existent
    credentials = None
    if os.path.exists(token_file):
        with open(token_file, "rb") as token:
            credentials = pickle.load(token)

    # Gérer le rafraîchissement des credentials
    if credentials:
        if credentials.expired and credentials.refresh_token:
            try:
                credentials.refresh(requests.Request())
                with open(token_file, "wb") as token:
                    pickle.dump(credentials, token)
                print("Credentials rafraîchies avec succès.")
            except Exception as e:
                print(f"Échec du rafraîchissement : {e}")
                credentials = None  # Forcer une nouvelle authentification si le rafraîchissement échoue
        elif not credentials.valid:
            credentials = None  # Forcer une nouvelle authentification si invalide sans refresh_token

    # Si pas de credentials ou invalides, lancer l'authentification
    if not credentials:
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            client_secrets_file, SCOPES)
        credentials = flow.run_local_server(port=8080)
        # Sauvegarder les credentials pour une utilisation future
        with open(token_file, "wb") as token:
            pickle.dump(credentials, token)
        print("Nouvelle authentification effectuée et sauvegardée.")

    print("API YouTube construite avec succès.")
    youtube = googleapiclient.discovery.build("youtube", "v3", credentials=credentials)
    return youtube

def upload_video(youtube, title, description, tags, media_file, thumbnail_file=None):
    request_body = {
        "snippet": {
            "categoryId": "22",
            "title": title,
            "description": description,
            "tags": tags
        },
        "status": {
            "privacyStatus": "public"  # Garantir publication immédiate
        }
    }

    if not os.path.exists(media_file):
        raise Exception(f"Le fichier vidéo {media_file} n'existe pas.")

    print(f"Début de l'upload du fichier : {media_file}")
    request = youtube.videos().insert(
        part="snippet,status",
        body=request_body,
        media_body=googleapiclient.http.MediaFileUpload(media_file, chunksize=1024*1024, resumable=True)
    )

    response = None
    while response is None:
        try:
            print("Attente du prochain chunk...")
            status, response = request.next_chunk()
            if status:
                print(f"Upload {int(status.progress() * 100)}%")
            else:
                print("Statut non disponible, vérification en cours...")
        except googleapiclient.errors.HttpError as e:
            print(f"Détails de l'erreur HTTP : {e.resp.status} - {e.content.decode()}")
            raise Exception(f"Erreur HTTP : {e}")
        except Exception as e:
            print(f"Détails de l'erreur : {e}")
            raise Exception(f"Erreur inattendue : {e}")

    video_id = response['id']
    print(f"Vidéo uploadée avec ID : {video_id}")

    # Ajout de la miniature si fournie
    if thumbnail_file and os.path.exists(thumbnail_file):
        print(f"Début de l'upload de la miniature : {thumbnail_file}")
        try:
            thumbnail_request = youtube.thumbnails().set(
                videoId=video_id,
                media_body=googleapiclient.http.MediaFileUpload(thumbnail_file)
            )
            thumbnail_response = thumbnail_request.execute()
            print(f"Miniature définie avec succès !")
        except googleapiclient.errors.HttpError as e:
            print(f"Échec de l'upload de la miniature : {e.resp.status} - {e.content.decode()}")
            print("Vérifiez les permissions de votre compte YouTube pour les miniatures.")

    # Vérifier et forcer le statut public si nécessaire
    video_response = youtube.videos().list(part="status", id=video_id).execute()
    current_status = video_response['items'][0]['status']['privacyStatus']
    print(f"Statut actuel de la vidéo : {current_status}")
    if current_status != "public":
        update_body = {
            "status": {
                "privacyStatus": "public"
            }
        }
        youtube.videos().update(part="status", body=update_body, id=video_id).execute()
        print("Statut forcé à 'public'.")

    return video_id

if __name__ == "__main__":
    try:
        youtube = authenticate_youtube()
        title = "Ma Vidéo Personnalisée"
        description = "Description !!!!!"
        tags = ["test", "personnalisé", "api"]
        media_file = "C:/Users/imane/Videos/Enregistrements d’écran/Enregistrement de l'écran 2025-07-22 094358.mp4"
        thumbnail_file = "C:/Users/imane/Downloads/img/R.jpeg"
        upload_video(youtube, title, description, tags, media_file, thumbnail_file)
    except Exception as e:
        print(f"Erreur globale : {e}")
