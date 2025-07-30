from playwright.sync_api import sync_playwright, TimeoutError
import json
import time


def pub_via_facebook():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()

        # Charger cookies
        with open("C:/Users/imane/Desktop/PY/cookies_fb.json", "r") as f:
            cookies = json.load(f)
        context.add_cookies(cookies)

        
        with open("C:/Users/imane/Desktop/PY/stealth_fb.min.js") as f:
            stealth_js = f.read()
        context.add_init_script(stealth_js)

        
        context.route("**/*", lambda route, request: route.abort() if request.resource_type in ["image", "media", "stylesheet"] else route.continue_())

        page = context.new_page()
        page.goto("https://www.facebook.com/", wait_until="domcontentloaded", timeout=60000)

        time.sleep(5)

        try:
            
            # Cliquer sur le bouton "What's on your mind"
            button = page.get_by_text("What's on your mind, Safae?").nth(0)
            button.click()
            print("Bouton modale cliqué")

            # Attendre la zone de texte
            textbox = page.locator('div[role="textbox"]')
            textbox.wait_for(state="visible", timeout=10000)
            textbox.fill("Hello  depuis playright + cookies + stealth + 2")
            print("Message rempli")

            time.sleep(1)

            # Cliquer sur le bouton "Post"
            publish_button = page.locator('div[aria-label="Post"]').nth(0)
            publish_button.wait_for(state="visible", timeout=5000)
            publish_button.click()
            print("Publication envoyée")

        except TimeoutError as e:
            print(f"Timeout sur un élément : {e}")
        except Exception as e:
            print(f"Erreur : {e}")

        time.sleep(5)
        browser.close()
pub_via_facebook()
