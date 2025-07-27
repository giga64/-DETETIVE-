#!/usr/bin/env python3
"""
Script para verificar se o Playwright está funcionando no Render
"""

import subprocess
import sys
import os

def check_playwright():
    """Verifica se o Playwright está funcionando"""
    print("🔍 Verificando Playwright no Render...")
    
    try:
        # Tenta importar
        from playwright.async_api import async_playwright
        print("✅ Playwright importado com sucesso!")
        
        # Verifica se o executável existe
        import asyncio
        
        async def test_launch():
            try:
                playwright = await async_playwright().start()
                browser = await playwright.chromium.launch(
                    headless=True,
                    args=[
                        '--no-sandbox',
                        '--disable-setuid-sandbox',
                        '--disable-dev-shm-usage'
                    ]
                )
                page = await browser.new_page()
                await page.goto('https://example.com')
                title = await page.title()
                print(f"✅ Navegador funcionando! Título: {title}")
                await browser.close()
                await playwright.stop()
                return True
            except Exception as e:
                print(f"❌ Erro ao testar navegador: {e}")
                return False
        
        # Executa o teste
        result = asyncio.run(test_launch())
        return result
        
    except ImportError as e:
        print(f"❌ Playwright não encontrado: {e}")
        print("📦 Tentando instalar...")
        
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "playwright"])
            subprocess.check_call([sys.executable, "-m", "playwright", "install", "chromium"])
            subprocess.check_call([sys.executable, "-m", "playwright", "install-deps"])
            print("✅ Playwright instalado! Execute novamente.")
            return True
        except Exception as e2:
            print(f"❌ Erro na instalação: {e2}")
            return False

if __name__ == "__main__":
    success = check_playwright()
    
    if success:
        print("\n🎉 Playwright está funcionando corretamente!")
    else:
        print("\n❌ Problemas com Playwright detectados.")
        print("💡 Verifique os logs do Render.") 