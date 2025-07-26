#!/usr/bin/env python3
"""
Módulo de consulta automatizada no site da OAB
https://cna.oab.org.br/
"""

import asyncio
import re
import time
from playwright.async_api import async_playwright
from typing import Optional, Dict, Any

class ConsultaOABAutomatizada:
    def __init__(self, profile_dir: str = "oab_profile"):
        self.profile_dir = profile_dir
        self.browser = None
        self.page = None
        
        # Mapeamento de estados para seccionais
        self.seccionais = {
            'AC': 'Conselho Seccional - Acre',
            'AL': 'Conselho Seccional - Alagoas',
            'AM': 'Conselho Seccional - Amazonas',
            'AP': 'Conselho Seccional - Amapá',
            'BA': 'Conselho Seccional - Bahia',
            'CE': 'Conselho Seccional - Ceará',
            'DF': 'Conselho Seccional - Distrito Federal',
            'ES': 'Conselho Seccional - Espirito Santo',
            'GO': 'Conselho Seccional - Goiás',
            'MA': 'Conselho Seccional - Maranhão',
            'MG': 'Conselho Seccional - Minas Gerais',
            'MS': 'Conselho Seccional - Mato Grosso do Sul',
            'MT': 'Conselho Seccional - Mato Grosso',
            'PA': 'Conselho Seccional - Pará',
            'PB': 'Conselho Seccional - Paraíba',
            'PE': 'Conselho Seccional - Pernambuco',
            'PI': 'Conselho Seccional - Piauí',
            'PR': 'Conselho Seccional - Paraná',
            'RJ': 'Conselho Seccional - Rio de Janeiro',
            'RN': 'Conselho Seccional - Rio Grande do Norte',
            'RO': 'Conselho Seccional - Rondônia',
            'RR': 'Conselho Seccional - Roraima',
            'RS': 'Conselho Seccional - Rio Grande do Sul',
            'SC': 'Conselho Seccional - Santa Catarina',
            'SE': 'Conselho Seccional - Sergipe',
            'SP': 'Conselho Seccional - São Paulo',
            'TO': 'Conselho Seccional - Tocantins'
        }
        
    async def __aenter__(self):
        """Context manager entry"""
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch_persistent_context(
            user_data_dir=self.profile_dir,
            headless=True  # True para produção
        )
        self.page = self.browser.pages[0] if self.browser.pages else await self.browser.new_page()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        if self.browser:
            await self.browser.close()
        if hasattr(self, 'playwright'):
            await self.playwright.stop()
    
    async def consultar_por_nome(self, nome: str, estado: str = "SP", tipo: str = "Advogado") -> Dict[str, Any]:
        """Consulta advogado por nome com preenchimento completo"""
        try:
            # Acessa o site da OAB
            await self.page.goto("https://cna.oab.org.br/")
            await self.page.wait_for_load_state("networkidle")
            
            # Preenche o nome
            await self.page.fill('input[name="nome"]', nome)
            
            # Seleciona a seccional (estado)
            seccional = self.seccionais.get(estado.upper(), "Conselho Seccional - São Paulo")
            await self.page.select_option('select[name="seccional"]', seccional)
            
            # Seleciona o tipo de inscrição
            await self.page.select_option('select[name="tipo"]', tipo)
            
            # Resolve o captcha (se houver)
            await self._resolver_captcha()
            
            # Clica em pesquisar
            await self.page.click('button[type="submit"]')
            
            # Aguarda resultado
            await self.page.wait_for_timeout(5000)
            
            # Captura o resultado
            resultado = await self._extrair_resultado()
            
            return {
                "sucesso": True,
                "tipo": "nome",
                "identificador": nome,
                "estado": estado,
                "resultado": resultado,
                "fonte": "OAB - https://cna.oab.org.br/"
            }
            
        except Exception as e:
            return {
                "sucesso": False,
                "erro": str(e),
                "tipo": "nome",
                "identificador": nome
            }
    
    async def consultar_por_inscricao(self, inscricao: str, estado: str = "SP", tipo: str = "Advogado") -> Dict[str, Any]:
        """Consulta advogado por inscrição com preenchimento completo"""
        try:
            await self.page.goto("https://cna.oab.org.br/")
            await self.page.wait_for_load_state("networkidle")
            
            # Preenche a inscrição
            await self.page.fill('input[name="inscricao"]', inscricao)
            
            # Seleciona a seccional
            seccional = self.seccionais.get(estado.upper(), "Conselho Seccional - São Paulo")
            await self.page.select_option('select[name="seccional"]', seccional)
            
            # Seleciona o tipo
            await self.page.select_option('select[name="tipo"]', tipo)
            
            # Resolve captcha
            await self._resolver_captcha()
            
            # Pesquisa
            await self.page.click('button[type="submit"]')
            await self.page.wait_for_timeout(5000)
            
            resultado = await self._extrair_resultado()
            
            return {
                "sucesso": True,
                "tipo": "inscricao",
                "identificador": inscricao,
                "estado": estado,
                "resultado": resultado,
                "fonte": "OAB - https://cna.oab.org.br/"
            }
            
        except Exception as e:
            return {
                "sucesso": False,
                "erro": str(e),
                "tipo": "inscricao",
                "identificador": inscricao
            }
    
    async def _resolver_captcha(self):
        """Tenta resolver o captcha automaticamente"""
        try:
            # Procura por checkbox de "Não sou um robô"
            captcha_selectors = [
                'input[type="checkbox"]',
                '.g-recaptcha',
                '#recaptcha',
                '[data-sitekey]'
            ]
            
            for selector in captcha_selectors:
                try:
                    elemento = await self.page.query_selector(selector)
                    if elemento:
                        await elemento.click()
                        await self.page.wait_for_timeout(2000)
                        break
                except:
                    continue
                    
        except Exception as e:
            print(f"⚠️ Aviso: Não foi possível resolver captcha automaticamente: {e}")
    
    async def _extrair_resultado(self) -> str:
        """Extrai o resultado da página"""
        try:
            # Aguarda carregamento da página
            await self.page.wait_for_timeout(3000)
            
            # Procura por elementos de resultado
            resultado_selectors = [
                '.resultado',
                '.search-result', 
                'table',
                '.content',
                '.advogado-info',
                '#resultado'
            ]
            
            for selector in resultado_selectors:
                try:
                    elementos = await self.page.query_selector_all(selector)
                    for elemento in elementos:
                        texto = await elemento.inner_text()
                        if texto and len(texto.strip()) > 20:
                            return self._limpar_texto(texto)
                except:
                    continue
            
            # Se não encontrar, pega todo o conteúdo da página
            conteudo = await self.page.content()
            return self._extrair_texto_relevante(conteudo)
            
        except Exception as e:
            return f"Erro ao extrair resultado: {str(e)}"
    
    def _limpar_texto(self, texto: str) -> str:
        """Limpa e formata o texto extraído"""
        # Remove espaços extras
        texto = re.sub(r'\s+', ' ', texto.strip())
        
        # Remove elementos HTML
        texto = re.sub(r'<[^>]+>', '', texto)
        
        # Remove caracteres especiais desnecessários
        texto = re.sub(r'[^\w\s\-\.\,\:\;\(\)]', '', texto)
        
        return texto
    
    def _extrair_texto_relevante(self, html: str) -> str:
        """Extrai texto relevante do HTML"""
        # Remove scripts e styles
        html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
        html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL)
        
        # Extrai texto
        texto = re.sub(r'<[^>]+>', ' ', html)
        texto = re.sub(r'\s+', ' ', texto)
        
        # Pega linhas relevantes
        linhas = [linha.strip() for linha in texto.split('\n') if linha.strip()]
        return '\n'.join(linhas[:30])  # Primeiras 30 linhas

# Função principal para uso no app.py
async def consulta_oab_completa(identificador: str, estado: str = "SP", tipo: str = "Advogado") -> str:
    """Função principal para consulta OAB completa"""
    async with ConsultaOABAutomatizada() as oab:
        # Detecta se é inscrição ou nome
        if re.match(r'^\d+$', identificador):
            resultado = await oab.consultar_por_inscricao(identificador, estado, tipo)
        else:
            resultado = await oab.consultar_por_nome(identificador, estado, tipo)
        
        if resultado["sucesso"]:
            return f"""
🔍 CONSULTA OAB - {resultado['tipo'].upper()}
📋 Identificador: {resultado['identificador']}
🏛️ Estado: {resultado['estado']}
👤 Tipo: {tipo}
🌐 Fonte: {resultado['fonte']}

{resultado['resultado']}
            """.strip()
        else:
            return f"❌ Erro na consulta OAB: {resultado.get('erro', 'Erro desconhecido')}" 