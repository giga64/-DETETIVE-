#!/usr/bin/env python3
"""
Script de teste para a funcionalidade OAB
"""

import re
import sys
import os

# Adiciona o diretório atual ao path para importar funções do app.py
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_oab_validation():
    """Testa as funções de validação de OAB"""
    print("🧪 Testando validação de OAB...")
    print("=" * 50)
    
    # Importa funções do app.py
    try:
        from app import normalize_oab, is_oab, get_oab_command
    except ImportError as e:
        print(f"❌ Erro ao importar funções: {e}")
        return False
    
    # Casos de teste
    test_cases = [
        # (entrada, esperado_normalizado, esperado_valido, esperado_comando)
        ("123456/SP", "123456SP", True, "/oab 123456/SP"),
        ("123456SP", "123456SP", True, "/oab 123456/SP"),
        ("123456", "123456", True, "/oab 123456/SP"),
        ("123456/SP ", "123456SP", True, "/oab 123456/SP"),
        ("123456/SPA", "123456SPA", False, "/oab 123456/SPA"),
        ("12345/SP", "12345SP", False, "/oab 12345/SP"),
        ("123456/", "123456", True, "/oab 123456/SP"),
        ("123456/RJ", "123456RJ", True, "/oab 123456/RJ"),
        ("123456/RJ", "123456RJ", True, "/oab 123456/RJ"),
        ("abc123/SP", "ABC123SP", False, "/oab ABC123SP"),
    ]
    
    passed = 0
    total = len(test_cases)
    
    for i, (input_val, expected_norm, expected_valid, expected_cmd) in enumerate(test_cases, 1):
        print(f"\n📝 Teste {i}: '{input_val}'")
        
        # Testa normalização
        normalized = normalize_oab(input_val)
        norm_ok = normalized == expected_norm
        print(f"   Normalização: {normalized} {'✅' if norm_ok else '❌'}")
        
        # Testa validação
        is_valid = is_oab(input_val)
        valid_ok = is_valid == expected_valid
        print(f"   Validação: {is_valid} {'✅' if valid_ok else '❌'}")
        
        # Testa comando
        if is_valid:
            command = get_oab_command(input_val)
            cmd_ok = command == expected_cmd
            print(f"   Comando: {command} {'✅' if cmd_ok else '❌'}")
        else:
            print(f"   Comando: N/A (inválido)")
            cmd_ok = True
        
        if norm_ok and valid_ok and cmd_ok:
            passed += 1
            print(f"   Resultado: ✅ PASSOU")
        else:
            print(f"   Resultado: ❌ FALHOU")
    
    print(f"\n📊 Resultado: {passed}/{total} testes passaram")
    return passed == total

def test_cpf_cnpj_compatibility():
    """Testa se as funções de CPF/CNPJ ainda funcionam"""
    print("\n🧪 Testando compatibilidade CPF/CNPJ...")
    print("=" * 50)
    
    try:
        from app import normalize, is_cpf, is_cnpj
    except ImportError as e:
        print(f"❌ Erro ao importar funções: {e}")
        return False
    
    # Testes CPF
    cpf_tests = [
        ("123.456.789-01", "12345678901", True),
        ("12345678901", "12345678901", True),
        ("123.456.789-0", "1234567890", False),
        ("123456789012", "123456789012", False),
    ]
    
    # Testes CNPJ
    cnpj_tests = [
        ("12.345.678/0001-90", "12345678000190", True),
        ("12345678000190", "12345678000190", True),
        ("12.345.678/0001-9", "1234567800019", False),
        ("123456789012345", "123456789012345", False),
    ]
    
    passed = 0
    total = len(cpf_tests) + len(cnpj_tests)
    
    print("📝 Testes CPF:")
    for input_val, expected_norm, expected_valid in cpf_tests:
        normalized = normalize(input_val)
        is_valid = is_cpf(normalized)
        
        norm_ok = normalized == expected_norm
        valid_ok = is_valid == expected_valid
        
        print(f"   '{input_val}' -> {normalized} (válido: {is_valid}) {'✅' if norm_ok and valid_ok else '❌'}")
        
        if norm_ok and valid_ok:
            passed += 1
    
    print("\n📝 Testes CNPJ:")
    for input_val, expected_norm, expected_valid in cnpj_tests:
        normalized = normalize(input_val)
        is_valid = is_cnpj(normalized)
        
        norm_ok = normalized == expected_norm
        valid_ok = is_valid == expected_valid
        
        print(f"   '{input_val}' -> {normalized} (válido: {is_valid}) {'✅' if norm_ok and valid_ok else '❌'}")
        
        if norm_ok and valid_ok:
            passed += 1
    
    print(f"\n📊 Resultado: {passed}/{total} testes passaram")
    return passed == total

def test_form_validation():
    """Testa a lógica de validação do formulário"""
    print("\n🧪 Testando validação de formulário...")
    print("=" * 50)
    
    try:
        from app import normalize_oab, is_oab, normalize, is_cpf, is_cnpj
    except ImportError as e:
        print(f"❌ Erro ao importar funções: {e}")
        return False
    
    # Simula dados do formulário
    test_cases = [
        # (tipo_consulta, identificador, esperado_valido, esperado_tipo)
        ("cpf_cnpj", "123.456.789-01", True, "CPF"),
        ("cpf_cnpj", "12.345.678/0001-90", True, "CNPJ"),
        ("cpf_cnpj", "123456789", False, "INVALIDO"),
        ("oab", "123456/SP", True, "OAB"),
        ("oab", "123456SP", True, "OAB"),
        ("oab", "123456", True, "OAB"),
        ("oab", "12345/SP", False, "INVALIDO"),
        ("oab", "abc123/SP", False, "INVALIDO"),
    ]
    
    passed = 0
    total = len(test_cases)
    
    for tipo_consulta, identificador, expected_valid, expected_tipo in test_cases:
        print(f"\n📝 Teste: {tipo_consulta} -> '{identificador}'")
        
        if tipo_consulta == "oab":
            normalized = normalize_oab(identificador)
            is_valid = is_oab(normalized)
            tipo = "OAB" if is_valid else "INVALIDO"
        else:
            normalized = normalize(identificador)
            if is_cpf(normalized):
                tipo = "CPF"
                is_valid = True
            elif is_cnpj(normalized):
                tipo = "CNPJ"
                is_valid = True
            else:
                tipo = "INVALIDO"
                is_valid = False
        
        valid_ok = is_valid == expected_valid
        tipo_ok = tipo == expected_tipo
        
        print(f"   Normalizado: {normalized}")
        print(f"   Válido: {is_valid} {'✅' if valid_ok else '❌'}")
        print(f"   Tipo: {tipo} {'✅' if tipo_ok else '❌'}")
        
        if valid_ok and tipo_ok:
            passed += 1
            print(f"   Resultado: ✅ PASSOU")
        else:
            print(f"   Resultado: ❌ FALHOU")
    
    print(f"\n📊 Resultado: {passed}/{total} testes passaram")
    return passed == total

def main():
    """Função principal de teste"""
    print("🔍 Testando funcionalidade OAB")
    print("=" * 60)
    
    # Executa todos os testes
    tests = [
        ("Validação OAB", test_oab_validation),
        ("Compatibilidade CPF/CNPJ", test_cpf_cnpj_compatibility),
        ("Validação de Formulário", test_form_validation),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Erro no teste {test_name}: {e}")
            results.append((test_name, False))
    
    # Resumo final
    print(f"\n{'='*60}")
    print("📊 RESUMO DOS TESTES")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSOU" if result else "❌ FALHOU"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 Resultado Final: {passed}/{total} testes passaram")
    
    if passed == total:
        print("🎉 Todos os testes passaram! A funcionalidade OAB está funcionando corretamente.")
        return True
    else:
        print("⚠️ Alguns testes falharam. Verifique a implementação.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 