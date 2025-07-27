#!/usr/bin/env python3
"""
Módulo de consulta automatizada no site da OAB
https://cna.oab.org.br/
"""

import asyncio
import re
import time
import subprocess
import sys
import os
from typing import Optional, Dict, Any

# Tenta importar Playwright, se não conseguir, instala
try:
    from playwright.async_api import async_playwright
except ImportError:
    print("📦 Instalando Playwright...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "playwright"])
    subprocess.check_call([sys.executable, "-m", "playwright", "install", "chromium"])
    from playwright.async_api import async_playwright

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
        try:
            self.playwright = await async_playwright().start()
            
            # Configurações específicas para Render
            browser_args = [
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-dev-shm-usage',
                '--disable-accelerated-2d-canvas',
                '--no-first-run',
                '--no-zygote',
                '--disable-gpu',
                '--disable-web-security',
                '--disable-features=VizDisplayCompositor'
            ]
            
            # Tenta usar launch_persistent_context primeiro
            try:
                self.browser = await self.playwright.chromium.launch_persistent_context(
                    user_data_dir=self.profile_dir,
                    headless=True,
                    args=browser_args,
                    ignore_default_args=['--disable-extensions']
                )
            except Exception as e:
                print(f"⚠️ Erro com launch_persistent_context: {e}")
                print("🔄 Tentando launch simples...")
                
                # Fallback para launch simples
                self.browser = await self.playwright.chromium.launch(
                    headless=True,
                    args=browser_args
                )
                self.page = await self.browser.new_page()
                return self
            
            self.page = self.browser.pages[0] if self.browser.pages else await self.browser.new_page()
            return self
            
        except Exception as e:
            print(f"❌ Erro ao inicializar Playwright: {e}")
            # Tenta instalar o Playwright se necessário
            try:
                print("📦 Tentando instalar Playwright...")
                subprocess.check_call([sys.executable, "-m", "playwright", "install", "chromium"])
                subprocess.check_call([sys.executable, "-m", "playwright", "install-deps"])
                print("✅ Playwright instalado, tentando novamente...")
                
                # Tenta novamente
                self.playwright = await async_playwright().start()
                
                # Tenta launch simples primeiro
                try:
                    self.browser = await self.playwright.chromium.launch(
                        headless=True,
                        args=browser_args
                    )
                    self.page = await self.browser.new_page()
                    return self
                except Exception as e2:
                    print(f"❌ Erro persistente com launch: {e2}")
                    raise e2
                    
            except Exception as e2:
                print(f"❌ Erro persistente: {e2}")
                raise e2
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        if self.browser:
            try:
                await self.browser.close()
            except:
                pass
        if hasattr(self, 'playwright'):
            try:
                await self.playwright.stop()
            except:
                pass
    
    async def consultar_por_nome(self, nome: str, estado: str = "SP", tipo: str = "Advogado") -> Dict[str, Any]:
        """Consulta advogado por nome com preenchimento completo"""
        try:
            # Acessa o site da OAB
            await self.page.goto("https://cna.oab.org.br/", wait_until="networkidle", timeout=30000)
            
            # Aguarda carregamento da página
            await self.page.wait_for_timeout(3000)
            
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
            await self.page.goto("https://cna.oab.org.br/", wait_until="networkidle", timeout=30000)
            await self.page.wait_for_timeout(3000)
            
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
        """Extrai o resultado da página incluindo informações detalhadas"""
        try:
            # Aguarda carregamento da página
            await self.page.wait_for_timeout(3000)
            
            # Primeiro, tenta extrair resultados básicos
            resultado_basico = await self._extrair_resultado_basico()
            
            # Depois, tenta clicar nos resultados para obter detalhes
            resultado_detalhado = await self._extrair_resultado_detalhado()
            
            # Combina os resultados
            if resultado_detalhado:
                return f"{resultado_basico}\n\n{resultado_detalhado}"
            else:
                return resultado_basico
            
        except Exception as e:
            return f"Erro ao extrair resultado: {str(e)}"
    
    async def _extrair_resultado_basico(self) -> str:
        """Extrai o resultado básico da página"""
        try:
            # Procura pela seção RESULTADO
            resultado_selectors = [
                '.resultado',
                '#resultado',
                'div:has-text("RESULTADO")',
                'table',
                '.search-result'
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
            
            # Se não encontrar seção específica, pega conteúdo geral
            conteudo = await self.page.content()
            return self._extrair_texto_relevante(conteudo)
            
        except Exception as e:
            return f"Erro ao extrair resultado básico: {str(e)}"
    
    async def _extrair_resultado_detalhado(self) -> str:
        """Extrai informações detalhadas clicando nos resultados"""
        try:
            # Procura por links ou elementos clicáveis nos resultados
            clickable_selectors = [
                'a[href*="detalhes"]',
                'a[href*="ficha"]',
                '.resultado a',
                'table a',
                '.search-result a',
                'tr[onclick]',
                '.clickable'
            ]
            
            detalhes_encontrados = []
            
            for selector in clickable_selectors:
                try:
                    elementos = await self.page.query_selector_all(selector)
                    for i, elemento in enumerate(elementos[:3]):  # Limita a 3 cliques
                        try:
                            # Clica no elemento
                            await elemento.click()
                            await self.page.wait_for_timeout(2000)
                            
                            # Extrai informações do pop-up ou nova página
                            detalhes = await self._extrair_detalhes_popup()
                            if detalhes:
                                detalhes_encontrados.append(f"--- DETALHES {i+1} ---\n{detalhes}")
                            
                            # Fecha pop-up se houver
                            await self._fechar_popup()
                            
                        except Exception as e:
                            print(f"Erro ao clicar no elemento {i}: {e}")
                            continue
                            
                except:
                    continue
            
            if detalhes_encontrados:
                return "\n\n".join(detalhes_encontrados)
            else:
                return ""
                
        except Exception as e:
            return f"Erro ao extrair detalhes: {str(e)}"
    
    async def _extrair_detalhes_popup(self) -> str:
        """Extrai informações detalhadas do pop-up"""
        try:
            # Procura por pop-ups ou modais
            popup_selectors = [
                '.modal',
                '.popup',
                '.dialog',
                '[role="dialog"]',
                '.ficha',
                '.detalhes'
            ]
            
            for selector in popup_selectors:
                try:
                    popup = await self.page.query_selector(selector)
                    if popup:
                        texto = await popup.inner_text()
                        if texto and len(texto.strip()) > 50:
                            return self._limpar_texto(texto)
                except:
                    continue
            
            # Se não encontrar pop-up, tenta extrair da página atual
            conteudo = await self.page.content()
            return self._extrair_texto_relevante(conteudo)
            
        except Exception as e:
            return f"Erro ao extrair pop-up: {str(e)}"
    
    async def _fechar_popup(self):
        """Tenta fechar pop-ups abertos"""
        try:
            # Procura por botões de fechar
            close_selectors = [
                '.close',
                '.fechar',
                '[aria-label="Close"]',
                '.modal .close',
                '.popup .close',
                'button:has-text("X")',
                'button:has-text("Fechar")'
            ]
            
            for selector in close_selectors:
                try:
                    close_btn = await self.page.query_selector(selector)
                    if close_btn:
                        await close_btn.click()
                        await self.page.wait_for_timeout(1000)
                        break
                except:
                    continue
                    
        except Exception as e:
            print(f"Erro ao fechar pop-up: {e}")
    
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
        return '\n'.join(linhas[:50])  # Primeiras 50 linhas

# Função principal para uso no app.py
async def consulta_oab_completa(identificador: str, estado: str = "SP", tipo: str = "Advogado") -> str:
    """Função principal para consulta OAB completa"""
    try:
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
    except Exception as e:
        return f"❌ Erro crítico na consulta OAB: {str(e)}" 