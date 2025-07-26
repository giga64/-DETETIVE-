#!/bin/bash

echo "🚀 Iniciando build para Render..."

# Instala dependências Python
echo "📦 Instalando dependências Python..."
pip install -r requirements.txt

# Instala Playwright e navegadores
echo "🌐 Instalando Playwright..."
playwright install chromium

# Instala dependências do sistema (se necessário)
echo "🔧 Instalando dependências do sistema..."
playwright install-deps

echo "✅ Build concluído!"
echo "🚀 Sistema pronto para deploy no Render." 