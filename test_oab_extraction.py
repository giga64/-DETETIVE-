#!/usr/bin/env python3
"""
Script de teste para verificar extração de dados da CNA OAB
"""

import asyncio
from consulta_oab import ConsultaOABAutomatizada

async def test_extraction():
    """Testa a extração de dados da CNA"""
    print("🧪 Testando extração de dados da CNA OAB...")
    
    async with ConsultaOABAutomatizada() as oab:
        # Teste com um nome conhecido
        print("📋 Testando consulta por nome...")
        resultado = await oab.consultar_por_nome("MARCOS DÉLLI RIBEIRO RODRIGUES", "RN", "Advogado")
        
        if resultado["sucesso"]:
            print("✅ Consulta bem-sucedida!")
            print("📄 Resultado:")
            print(resultado["resultado"])
        else:
            print(f"❌ Erro na consulta: {resultado.get('erro')}")
        
        print("\n" + "="*50 + "\n")
        
        # Teste com inscrição
        print("📋 Testando consulta por inscrição...")
        resultado = await oab.consultar_por_inscricao("5553", "RN", "Advogado")
        
        if resultado["sucesso"]:
            print("✅ Consulta bem-sucedida!")
            print("📄 Resultado:")
            print(resultado["resultado"])
        else:
            print(f"❌ Erro na consulta: {resultado.get('erro')}")

if __name__ == "__main__":
    asyncio.run(test_extraction()) 