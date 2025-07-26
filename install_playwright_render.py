#!/usr/bin/env python3
"""
Script para instalar Playwright no ambiente Render
"""

import subprocess
import sys
import os

def install_playwright():
    """Instala Playwright e navegadores no ambiente Render"""
    print("🚀 Instalando Playwright para ambiente Render...")
    
    try:
        # Instala o Playwright
        print("📦 Instalando Playwright...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "playwright"])
        
        # Instala o Chromium
        print("🌐 Instalando Chromium...")
        subprocess.check_call([sys.executable, "-m", "playwright", "install", "chromium"])
        
        # Verifica a instalação
        print("✅ Verificando instalação...")
        subprocess.check_call([sys.executable, "-m", "playwright", "install-deps"])
        
        print("🎉 Playwright instalado com sucesso!")
        print("🚀 O sistema OAB está pronto para uso.")
        
    except Exception as e:
        print(f"❌ Erro na instalação: {e}")
        print("💡 Tentando método alternativo...")
        
        try:
            # Método alternativo
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "playwright"])
            subprocess.check_call([sys.executable, "-m", "playwright", "install", "--with-deps", "chromium"])
            print("✅ Instalação alternativa bem-sucedida!")
        except Exception as e2:
            print(f"❌ Erro na instalação alternativa: {e2}")
            return False
    
    return True

if __name__ == "__main__":
    print("🏛️ Configuração Playwright para Render")
    print("=" * 50)
    
    success = install_playwright()
    
    if success:
        print("\n✅ Configuração concluída!")
        print("🚀 O sistema OAB está pronto para uso no Render.")
    else:
        print("\n❌ Configuração falhou!")
        print("💡 Verifique os logs e tente novamente.") 