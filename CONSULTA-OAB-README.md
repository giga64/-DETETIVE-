# 🏛️ Sistema de Consulta OAB - Detetive

## 📋 **Visão Geral**

O sistema agora inclui **consultas automatizadas no site da OAB** (https://cna.oab.org.br/), permitindo buscar advogados por nome ou número de inscrição.

## 🚀 **Funcionalidades**

### ✅ **Consultas Disponíveis**
- **Por Nome:** Busca advogados pelo nome completo
- **Por Inscrição:** Busca pelo número de inscrição OAB
- **Estados:** Todos os 27 estados brasileiros
- **Tipos:** Advogado, Estagiário, Suplementar

### 🔧 **Automação Completa**
- **Preenchimento automático** de formulários
- **Seleção automática** de estado e tipo
- **Resolução de captcha** (quando possível)
- **Extração inteligente** de resultados

## 📁 **Arquivos Criados**

```
-DETETIVE-/
├── consulta_oab.py              # Módulo principal de consulta
├── setup_oab.py                 # Script de configuração
├── templates/
│   └── consulta-oab.html        # Interface de consulta OAB
├── static/
│   └── modern-style.css         # Estilos atualizados
└── app.py                       # App principal atualizado
```

## 🛠️ **Instalação e Configuração**

### **1. Instalar Dependências**
```bash
pip install playwright
playwright install chromium
```

### **2. Configurar Perfil OAB**
```bash
python setup_oab.py
```

### **3. Iniciar Aplicação**
```bash
python app.py
```

## 🎯 **Como Usar**

### **Acessar Consulta OAB**
1. Acesse: `http://localhost:8000/consulta-oab`
2. Ou clique em "🏛️ Consulta OAB" na página principal

### **Fazer Consulta**
1. **Preencha os campos:**
   - **Nome:** João Silva Santos
   - **OU Inscrição:** 123456
   - **Estado:** São Paulo (padrão)
   - **Tipo:** Advogado (padrão)

2. **Clique em:** "🔍 Consultar OAB"

3. **Aguarde** o resultado automático

## 🔍 **Exemplos de Consulta**

### **Por Nome:**
```
Nome: João Silva Santos
Estado: SP
Tipo: Advogado
```

### **Por Inscrição:**
```
Inscrição: 123456
Estado: RJ
Tipo: Advogado
```

## ⚙️ **Configuração Avançada**

### **Estados Disponíveis:**
- AC, AL, AM, AP, BA, CE, DF, ES, GO, MA, MG, MS, MT
- PA, PB, PE, PI, PR, RJ, RN, RO, RR, RS, SC, SE, SP, TO

### **Tipos de Inscrição:**
- **Advogado:** Inscrição regular
- **Estagiário:** Estagiário de advocacia
- **Suplementar:** Inscrição suplementar

## 🔧 **Troubleshooting**

### **Erro: "Módulo OAB não disponível"**
```bash
# Verifique se o arquivo existe
ls consulta_oab.py

# Reinstale dependências
pip install playwright
playwright install chromium
```

### **Erro: "Não foi possível resolver captcha"**
```bash
# Execute o setup novamente
python setup_oab.py

# Configure manualmente o captcha
```

### **Erro: "Timeout na consulta"**
- Verifique a conexão com a internet
- Tente novamente em alguns minutos
- O site pode estar temporariamente indisponível

## 📊 **Logs e Monitoramento**

### **Logs de Consulta:**
```
🔍 CONSULTA OAB - NOME
📋 Identificador: João Silva Santos
🏛️ Estado: SP
👤 Tipo: Advogado
🌐 Fonte: OAB - https://cna.oab.org.br/

[Resultado da consulta...]
```

### **Logs de Erro:**
```
❌ Erro na consulta OAB: [Descrição do erro]
```

## 🎨 **Interface**

### **Página Principal:**
- Link "🏛️ Consulta OAB" adicionado
- Mantém o visual atual
- Navegação intuitiva

### **Página OAB:**
- Formulário completo com labels
- Seletores para estado e tipo
- Validação de campos
- Mensagens de erro claras

## 🔄 **Integração com Sistema Atual**

### **Histórico Unificado:**
- Consultas OAB aparecem no histórico
- Mesmo formato de resultado
- Compatível com sistema existente

### **Navegação:**
- Botão "🏠 Voltar ao Detetive"
- Botão "📋 Ver histórico"
- Tema escuro/claro mantido

## ⚠️ **Limitações**

### **Captcha:**
- Pode precisar de intervenção manual
- Depende da configuração do site

### **Rate Limiting:**
- O site pode limitar consultas
- Aguarde entre consultas

### **Estrutura do Site:**
- Mudanças no site podem quebrar a automação
- Monitoramento necessário

## 🚀 **Próximos Passos**

### **Melhorias Futuras:**
1. **Cache de consultas** OAB
2. **API REST** para consultas OAB
3. **Validação avançada** de nomes
4. **Histórico específico** para OAB
5. **Notificações** de novos resultados

### **Expansão:**
1. **Outros sites** de consulta
2. **Mais tipos** de busca
3. **Integração** com outros sistemas

## 📞 **Suporte**

### **Problemas Comuns:**
1. **Módulo não encontrado:** Verifique instalação
2. **Captcha não resolvido:** Execute setup_oab.py
3. **Timeout:** Verifique conexão
4. **Erro de site:** Aguarde e tente novamente

### **Contato:**
- Verifique os logs da aplicação
- Execute `python setup_oab.py` se necessário
- Monitore o console para erros

---

## 🎉 **Sistema Completo**

Agora você tem um sistema completo que:
- ✅ **Consulta CPF/CNPJ** via Telegram
- ✅ **Consulta OAB** automatizada
- ✅ **Histórico unificado**
- ✅ **Interface moderna**
- ✅ **Tema escuro/claro**
- ✅ **Navegação intuitiva**

**🚀 O Detetive agora é uma ferramenta completa de investigação digital!** 