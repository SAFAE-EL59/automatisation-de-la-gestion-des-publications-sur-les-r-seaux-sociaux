import requests
import hmac
import hashlib
import time

# Les identifiants mis à jour
app_id = "app_id"
app_secret = "app_secret"
access_token = "access_token"
ig_user_id = "ig_user_id"  

# Calcul de l'appsecret_proof
appsecret_proof = hmac.new(
    app_secret.encode('utf-8'),
    access_token.encode('utf-8'),
    hashlib.sha256
).hexdigest()


def post_to_instagram(caption=None, media_url=None, tagged_users=None, title=None):
    try:
        if not caption and not media_url:
            raise Exception("Au moins un texte ou un média (image/vidéo URL) doit être fourni.")
        
        appsecret_proof = hmac.new(
            app_secret.encode('utf-8'),
            access_token.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()

        if media_url:
            if media_url.lower().endswith(('.jpg', '.jpeg', '.png')):
                media_type = "IMAGE"
            elif media_url.lower().endswith(('.mp4', '.mov')):
                media_type = "VIDEO"
            else:
                raise Exception("Type de média non supporté. Utilisez JPG/JPEG/PNG pour image ou MP4/MOV pour vidéo.")

            url = f"https://graph.facebook.com/v23.0/{ig_user_id}/media"
            payload = {
                "media_type": media_type,
                "image_url": media_url if media_type == "IMAGE" else None,
                "video_url": media_url if media_type == "VIDEO" else None,
                "caption": caption if caption else (title if title else ""),
                "access_token": access_token,
                "appsecret_proof": appsecret_proof
            }
            if tagged_users:
                payload["tagged_users"] = ",".join(tagged_users)

            response = requests.post(url, data={k: v for k, v in payload.items() if v is not None})
            result = response.json()
            if "id" not in result:
                raise Exception(f"Erreur création conteneur : {result}")
            container_id = result["id"]

            time.sleep(5)
            publish_url = f"https://graph.facebook.com/v23.0/{ig_user_id}/media_publish"
            publish_payload = {
                "creation_id": container_id,
                "access_token": access_token,
                "appsecret_proof": appsecret_proof
            }
            publish_response = requests.post(publish_url, data=publish_payload)
            publish_result = publish_response.json()
            if "id" in publish_result:
                print(f"Post publié ! ID : {publish_result['id']}")
            else:
                raise Exception(f"Erreur publication : {publish_result}")
        else:
            if tagged_users:
                tag_info = f" avec tags: {', '.join(tagged_users)}"
            else:
                tag_info = ""
            raise Exception(f"Publication texte seule non supportée pour posts standards. Texte: '{caption}'{tag_info}. Ajoutez une image ou une vidéo.")

    except Exception as e:
        print("Erreur :", str(e))





def post_instagram_reel(video_url, text="", tagged_users=None):
    ig_user_id = "17841475901669861"
    access_token = "EAAHKQ5VHUQkBPPQaJVESrbszcPkUGFw2wFYNs7H75FWLbCzDwQPY3EDVEb3v8XqjlsBBZB8f2eQHTzJq7WxRlIRVoiwz8l6GVBjpQoMAe6bFZCe1WUnu0tZAtVg0khoUIsD983njZAJ4QIRk2dYlRfE8SC3VfUJNhI7KpuxRgftlprOUEvSofN6GVSOSyuKw9htK"
    try:
        if not video_url or not access_token:
            raise Exception("video_url et access_token sont requis.")

        create_url = f"https://graph.facebook.com/v23.0/{ig_user_id}/media"
        payload = {
            "media_type": "REELS",
            "video_url": video_url,
            "text": text,
            "access_token": access_token,
            
        }
        if tagged_users:
            payload["tagged_users"] = ",".join(tagged_users)

        create_response = requests.post(create_url, data=payload)
        create_result = create_response.json()

        if "id" not in create_result:
            raise Exception(f"Erreur création conteneur : {create_result}")

        container_id = create_result["id"]
        print(f"Conteneur créé avec ID : {container_id}")

       
        time.sleep(5)

        
        publish_url = f"https://graph.facebook.com/v23.0/{ig_user_id}/media_publish"
        publish_payload = {
            "creation_id": container_id,
            "access_token": access_token
        }
        publish_response = requests.post(publish_url, data=publish_payload)
        publish_result = publish_response.json()

        if "id" in publish_result:
            print(f"Reel publié ! ID : {publish_result['id']}")
            return publish_result["id"]
        else:
            raise Exception(f"Erreur publication : {publish_result}")

    except Exception as e:
        print("Erreur :", str(e))
        return None

# Exemple 
if __name__ == "__main__":
    
    video_url = "https://....mp4",
    text = "Mon premier Reel ! #Reels #Test"


    reel_id = post_instagram_reel( video_url, text)
    if reel_id:
        print(f"Reel publié avec succès, ID : {reel_id}")
# Exécution 
if __name__ == "__main__":
    try:
      post_to_instagram(
            caption="Test avec image  ",
           media_url="https://www.dpreview.com/files/p/articles/7952219469/google-imagen-lead-image.jpeg",     
     )
    except Exception as e:
       print("Erreur :", str(e))
