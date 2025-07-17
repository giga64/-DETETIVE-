from playwright.sync_api import sync_playwright
import os

TELEGRAM_PROFILE = "telegram_profile"
WHATSAPP_PROFILE = "whatsapp_profile"

def sync_login(profile_dir: str, url: str):
    os.makedirs(profile_dir, exist_ok=True)
    with sync_playwright() as pw:
        browser = pw.chromium.launch_persistent_context(user_data_dir=profile_dir, headless=False)
        page = browser.pages[0] if browser.pages else browser.new_page()
        page.goto(url)
        print(f"🚀 Faça login em {url} e, após autenticar, feche o browser.")
        input("Pressione ENTER após fechar o browser... ")
        browser.close()

if __name__ == "__main__":
    sync_login(TELEGRAM_PROFILE, "https://web.telegram.org/")
    sync_login(WHATSAPP_PROFILE, "https://web.whatsapp.com/")
