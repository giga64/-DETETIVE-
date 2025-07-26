# 🏛️ Sistema de Consulta OAB - Detetive

## 📋 **Visão Geral**

O sistema agora inclui **consultas automatizadas no site da OAB** (https://cna.oab.org.br/), permitindo buscar advogados por nome ou número de inscrição e **extrair informações detalhadas** como endereço, telefone, situação profissional e mais.

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
- **Captura de informações detalhadas** do pop-up da CNA

### 📊 **Informações Extraídas**
O sistema captura automaticamente:
- **Nome completo** do advogado
- **Número de inscrição** OAB
- **Estado/Seccional** de registro
- **Tipo de inscrição** (Advogado, Estagiário, etc.)
- **Endereço profissional** completo
- **Telefone profissional**
- **CEP** do endereço
- **Situação** da inscrição (Regular, Irregular, etc.)
- **Informações adicionais** do pop-up da CNA

## 📁 **Arquivos Criados**

```
-DETETIVE-/
├── consulta_oab.py              # Módulo principal de consulta
├── setup_oab.py                 # Script de configuração
├── install_playwright_render.py # Instalação Playwright para Render
├── test_oab_extraction.py       # Script de teste de extração
├── build.sh                     # Script de build para Render
├── render.yaml                  # Configuração Render
├── templates/
│   └── consulta-oab.html        # Interface de consulta OAB
├── static/
│   └── modern-style.css         # Estilos atualizados
└── app.py                       # App principal atualizado
```

## 🛠️ **Instalação e Configuração**

### **Para Ambiente Local:**

#### **1. Instalar Dependências**
```bash
pip install -r requirements.txt
```

#### **2. Instalar Playwright**
```bash
python install_playwright_render.py
```

#### **3. Configurar Perfil OAB (Opcional)**
```bash
python setup_oab.py
```

#### **4. Testar Extração (Opcional)**
```bash
python test_oab_extraction.py
```

#### **5. Iniciar Aplicação**
```bash
python app.py
```

### **Para Render (Produção):**

#### **1. Configuração Automática**
O Render irá automaticamente:
- Instalar dependências do `requirements.txt`
- Instalar Playwright e Chromium
- Configurar dependências do sistema

#### **2. Arquivos de Configuração**
- `render.yaml` - Configuração do serviço
- `build.sh` - Script de build personalizado
- `requirements.txt` - Dependências Python

#### **3. Deploy Automático**
O sistema detecta automaticamente se está no Render e:
- Instala Playwright se necessário
- Configura argumentos específicos para o ambiente
- Trata erros de instalação

## 🎯 **Como Usar**

### **Acessar Consulta OAB**
1. Acesse: `http://localhost:8000/consulta-oab` (local)
2. Ou clique em "🏛️ Consulta OAB" na página principal

### **Fazer Consulta**
1. **Preencha os campos:**
   - **Nome:** João Silva Santos
   - **OU Inscrição:** 123456
   - **Estado:** São Paulo (padrão)
   - **Tipo:** Advogado (padrão)

2. **Clique em:** "🔍 Consultar OAB"

3. **Aguarde** o resultado automático com informações detalhadas

## 🔍 **Exemplos de Consulta**

### **Por Nome:**
```
Nome: MARCOS DÉLLI RIBEIRO RODRIGUES
Estado: RN
Tipo: Advogado
```

### **Por Inscrição:**
```
Inscrição: 5553
Estado: RN
Tipo: Advogado
```

### **Resultado Esperado:**
```
🔍 CONSULTA OAB - NOME
📋 Identificador: MARCOS DÉLLI RIBEIRO RODRIGUES
🏛️ Estado: RN
👤 Tipo: Advogado
🌐 Fonte: OAB - https://cna.oab.org.br/

RESULTADO
Nome: MARCOS DÉLLI RIBEIRO RODRIGUES
Tipo: ADVOGADO
Inscrição: 5553
UF: RN

--- DETALHES 1 ---
Nome: MARCOS DÉLLI RIBEIRO RODRIGUES
Inscrição: 5553
Profissão: ADVOGADO
Seccional: RN
Subseção: CONSELHO SECCIONAL - RIO GRANDE DO NORTE
Endereço Profissional: RUA AÇU, Nº 572, TIROL
Cidade/Estado: NATAL - RN
CEP: 59020110
Telefone Profissional: (84) 3221-5400
Situação: SITUAÇÃO REGULAR
```

## ⚙️ **Configuração Avançada**

### **Estados Disponíveis:**
- AC, AL, AM, AP, BA, CE, DF, ES, GO, MA, MG, MS, MT
- PA, PB, PE, PI, PR, RJ, RN, RO, RR, RS, SC, SE, SP, TO

### **Tipos de Inscrição:**
- **Advogado:** Inscrição regular
- **Estagiário:** Estagiário de advocacia
- **Suplementar:** Inscrição suplementar

### **Processo de Extração:**
1. **Consulta básica** no formulário da CNA
2. **Extração** dos resultados iniciais
3. **Clique automático** nos resultados para abrir detalhes
4. **Captura** das informações do pop-up
5. **Fechamento** automático dos pop-ups
6. **Combinação** dos dados básicos e detalhados

## 🔧 **Troubleshooting**

### **Erro: "Módulo OAB não disponível"**
```bash
# Verifique se o arquivo existe
ls consulta_oab.py

# Reinstale dependências
pip install -r requirements.txt
python install_playwright_render.py
```

### **Erro: "Executable doesn't exist" (Render)**
```bash
# O sistema tenta instalar automaticamente
# Se persistir, verifique os logs do Render
```

### **Erro: "Não foi possível resolver captcha"**
```bash
# Execute o setup novamente (local)
python setup_oab.py

# Configure manualmente o captcha
```

### **Erro: "Timeout na consulta"**
- Verifique a conexão com a internet
- Tente novamente em alguns minutos
- O site pode estar temporariamente indisponível

### **Erro: "Não conseguiu extrair detalhes"**
- O sistema pode não conseguir clicar nos resultados
- Verifique se o site mudou a estrutura
- Execute o teste: `python test_oab_extraction.py`

## 📊 **Logs e Monitoramento**

### **Logs de Inicialização:**
```
✅ Módulo OAB carregado com sucesso!
✅ Playwright já está instalado!
🚀 Sistema pronto para uso.
```

### **Logs de Consulta:**
```
🔍 CONSULTA OAB - NOME
📋 Identificador: MARCOS DÉLLI RIBEIRO RODRIGUES
🏛️ Estado: RN
👤 Tipo: Advogado
🌐 Fonte: OAB - https://cna.oab.org.br/

[Resultado detalhado com informações completas...]
```

### **Logs de Erro:**
```
❌ Erro na consulta OAB: [Descrição do erro]
❌ Erro crítico na consulta OAB: [Descrição do erro]
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

### **Ambiente Render:**
- Primeira execução pode ser mais lenta
- Dependências são instaladas automaticamente

### **Extração de Detalhes:**
- Depende da estrutura atual do site
- Pode não funcionar se o site mudar
- Pop-ups podem não abrir corretamente

## 🚀 **Próximos Passos**

### **Melhorias Futuras:**
1. **Cache de consultas** OAB
2. **API REST** para consultas OAB
3. **Validação avançada** de nomes
4. **Histórico específico** para OAB
5. **Notificações** de novos resultados
6. **Extração de fotos** dos advogados
7. **Informações de sociedade** (se disponível)

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
5. **Erro no Render:** Verifique logs de build
6. **Detalhes não extraídos:** Execute test_oab_extraction.py

### **Contato:**
- Verifique os logs da aplicação
- Execute `python install_playwright_render.py` se necessário
- Monitore o console para erros
- Use `python test_oab_extraction.py` para testar extração

---

## 🎉 **Sistema Completo**

Agora você tem um sistema completo que:
- ✅ **Consulta CPF/CNPJ** via Telegram
- ✅ **Consulta OAB** automatizada
- ✅ **Extração detalhada** de informações
- ✅ **Histórico unificado**
- ✅ **Interface moderna**
- ✅ **Tema escuro/claro**
- ✅ **Navegação intuitiva**
- ✅ **Compatível com Render**

**🚀 O Detetive agora é uma ferramenta completa de investigação digital com extração detalhada da CNA!** 