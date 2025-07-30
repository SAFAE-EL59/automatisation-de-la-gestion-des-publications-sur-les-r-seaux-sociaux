from playwright.sync_api import sync_playwright, TimeoutError
import time

def pub_photo_story_via_facebook():
    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            user_data_dir="C:/Users/imane/Desktop/TP/facebook_profile",
            headless=False
        )

        page = context.pages[0] if context.pages else context.new_page()

        page.goto("https://www.facebook.com/", wait_until="domcontentloaded", timeout=60000)
        print(" Page Facebook chargée")

        if "login" in page.url:
            print(" Connecte-toi manuellement une seule fois.")
            input(" Appuie sur Entrée une fois connecté...")

        try:
            page.get_by_role("link", name="Create story").click(timeout=10000)
            print(" Bouton 'Create Story' cliqué")
            time.sleep(3)

            page.get_by_text("Create a Photo Story").click(timeout=10000)
            print(" Option 'Photo Story' sélectionnée")
            time.sleep(3)

            input_file = page.locator("input[type='file']").nth(1)
            input_file.set_input_files(r"C:\Users\imane\Downloads\img\R.jpeg")
            print(" Image chargée via set_input_files")

            print(" Attente que le bouton 'Share to Story' soit activable...")
            share_button = page.locator('[aria-label="Share to Story"]')

            # Boucle d'attente côté Python sans wait_for_function (compatible CSP)
            timeout = 30  # secondes
            elapsed = 0
            while elapsed < timeout:
                aria_disabled = share_button.get_attribute("aria-disabled")
                if aria_disabled is None:
                    break  # bouton activable
                time.sleep(0.5)
                elapsed += 0.5
            else:
                raise TimeoutError("Bouton 'Share to Story' toujours désactivé après 30s")

            share_button.click()
            print(" Story publiée")

            time.sleep(5)

        except TimeoutError as e:
            print(f" Timeout : {e}")
        except Exception as e:
            print(f" Erreur : {e}")

        context.close()

pub_photo_story_via_facebook()
