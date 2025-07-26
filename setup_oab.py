#!/usr/bin/env python3
"""
Script para configurar o perfil do navegador para consultas OAB
"""

from playwright.sync_api import sync_playwright
import os

OAB_PROFILE = "oab_profile"

def setup_oab():
    """Configura o perfil do navegador para OAB"""
    os.makedirs(OAB_PROFILE, exist_ok=True)
    
    with sync_playwright() as pw:
        browser = pw.chromium.launch_persistent_context(
            user_data_dir=OAB_PROFILE, 
            headless=False
        )
        page = browser.pages[0] if browser.pages else browser.new_page()
        
        # Acessa o site da OAB
        print("🌐 Acessando o site da OAB...")
        page.goto("https://cna.oab.org.br/")
        
        print("✅ Site da OAB carregado!")
        print("💡 Configure o navegador conforme necessário.")
        print("📝 O sistema salvará as configurações para consultas automáticas.")
        print("🔧 Você pode configurar:")
        print("   - Resolver captchas manualmente")
        print("   - Aceitar cookies se necessário")
        print("   - Configurar preferências do site")
        
        input("\n⏳ Pressione ENTER quando terminar a configuração... ")
        browser.close()
        
        print("✅ Configuração OAB concluída!")
        print("🚀 O sistema agora pode fazer consultas automatizadas.")

if __name__ == "__main__":
    print("🏛️ Configuração do Sistema OAB")
    print("=" * 40)
    setup_oab() 