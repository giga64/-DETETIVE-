# Solução para Erro "database is locked"

## Problema
O erro `sqlite3.OperationalError: database is locked` ocorre quando múltiplas conexões tentam acessar o arquivo de sessão do Telethon (`bot_session.session`) simultaneamente.

## Causas Comuns
1. **Múltiplas instâncias da aplicação rodando**
2. **Conexões não fechadas adequadamente**
3. **Arquivo de sessão corrompido**
4. **Processos Python órfãos**

## Soluções Implementadas

### 1. Melhorias no Código Principal (`app.py`)

✅ **Implementado:**
- Sistema de lock para sincronizar acesso ao Telethon
- Context manager para gerenciar conexões de forma segura
- Tratamento robusto de erros
- Desconexão automática de clientes

### 2. Scripts de Diagnóstico e Correção

#### `fix_session.py`
```bash
python fix_session.py
```
- Verifica integridade do arquivo de sessão
- Detecta problemas de lock
- Faz backup automático se necessário
- Remove arquivo corrompido se for o caso

#### `restart_app.py`
```bash
python restart_app.py
```
- Para todos os processos Python da aplicação
- Verifica arquivo de sessão
- Reinicia a aplicação de forma limpa

## Como Resolver o Problema

### Passo 1: Parar Todos os Processos
```bash
# No Windows
taskkill /f /im python.exe

# No Linux/Mac
pkill -f python
```

### Passo 2: Verificar Arquivo de Sessão
```bash
python fix_session.py
```

### Passo 3: Se Necessário, Recriar Sessão
```bash
# Se o arquivo foi removido ou corrompido
python setup_login.py
```

### Passo 4: Reiniciar Aplicação
```bash
python restart_app.py
```

## Verificações Adicionais

### Verificar Processos Ativos
```bash
# Windows
tasklist | findstr python

# Linux/Mac
ps aux | grep python
```

### Verificar Arquivo de Sessão
```bash
# Verificar se existe
ls -la bot_session.session

# Verificar tamanho
stat bot_session.session
```

### Limpar Cache (se necessário)
```bash
# Remover arquivos temporários
rm -f *.session-journal
rm -f *.session-wal
```

## Prevenção

### 1. Sempre Use os Scripts de Reinicialização
```bash
python restart_app.py
```

### 2. Monitore Logs
Fique atento a mensagens de erro relacionadas a:
- "database is locked"
- "sqlite3.OperationalError"
- Problemas de conexão

### 3. Backup Regular
```bash
# Fazer backup do arquivo de sessão
cp bot_session.session bot_session_backup_$(date +%Y%m%d_%H%M%S).session
```

## Estrutura de Arquivos

```
-DETETIVE-/
├── app.py                    # Aplicação principal (melhorada)
├── fix_session.py           # Script de diagnóstico
├── restart_app.py           # Script de reinicialização
├── setup_login.py           # Configuração inicial
├── bot_session.session      # Arquivo de sessão do Telethon
└── requirements.txt         # Dependências (inclui psutil)
```

## Logs de Erro Comuns

### Erro Original
```
sqlite3.OperationalError: database is locked
```

### Solução Aplicada
- ✅ Lock de thread para sincronização
- ✅ Context manager para conexões
- ✅ Tratamento de erros robusto
- ✅ Desconexão automática

## Contato e Suporte

Se o problema persistir após seguir estas instruções:

1. Execute `python fix_session.py` e verifique a saída
2. Verifique se há múltiplos processos Python rodando
3. Considere recriar o arquivo de sessão com `setup_login.py`
4. Monitore os logs da aplicação para identificar padrões

## Notas Importantes

- ⚠️ **Nunca delete o arquivo `bot_session.session` sem fazer backup**
- 🔄 **Sempre use `restart_app.py` para reiniciar a aplicação**
- 📊 **Monitore o uso de memória e CPU dos processos Python**
- 💾 **Faça backups regulares do arquivo de sessão** 