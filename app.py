import os
import re
import asyncio
import sqlite3
import threading
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from telethon import TelegramClient, events

# ----------------------
# Configurações de diretórios
# ----------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

# ----------------------
# Banco de dados SQLite para histórico
# ----------------------
DB_FILE = os.path.join(BASE_DIR, "history.db")
conn = sqlite3.connect(DB_FILE, check_same_thread=False)
cursor = conn.cursor()

# Cria nova tabela sem dependência de IP
cursor.execute("""
CREATE TABLE IF NOT EXISTS searches_new (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    identifier   TEXT,
    response     TEXT,
    searched_at  DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")
conn.commit()

# Migra dados da tabela antiga se existir
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='searches'")
if cursor.fetchone():
    cursor.execute("""
        INSERT INTO searches_new (identifier, response, searched_at)
        SELECT identifier, response, searched_at FROM searches
        WHERE identifier IS NOT NULL
    """)
    cursor.execute("DROP TABLE searches")
    conn.commit()

# Renomeia a nova tabela
cursor.execute("ALTER TABLE searches_new RENAME TO searches")
conn.commit()

# ----------------------
# Configuração Telethon (Telegram)
# ----------------------
API_ID = 24383113
API_HASH = '387f7520aae351ddc83fb457cdb60085'
SESSION_NAME = 'bot_session'
GROUP_ID = -1002874013146

# Lock para sincronizar acesso ao Telethon
telegram_lock = threading.Lock()

# ----------------------
# Validação CPF/CNPJ/OAB
# ----------------------
CPF_RE = re.compile(r"^\d{11}$")
CNPJ_RE = re.compile(r"^\d{14}$")
OAB_RE = re.compile(r"^(\d{6})([A-Z]{2})$")

def normalize(id_str: str) -> str:
    return re.sub(r"\D", "", id_str)

def normalize_oab(oab_str: str) -> str:
    """Normaliza OAB removendo caracteres especiais e formatando"""
    # Remove tudo exceto números e letras
    cleaned = re.sub(r"[^A-Za-z0-9]", "", oab_str.upper())
    
    # Se tem 8 caracteres (6 números + 2 letras)
    if len(cleaned) == 8:
        numbers = cleaned[:6]
        letters = cleaned[6:8]
        return f"{numbers}{letters}"
    
    # Se tem 7 caracteres (6 números + 1 letra)
    elif len(cleaned) == 7:
        numbers = cleaned[:6]
        letter = cleaned[6]
        return f"{numbers}{letter}"
    
    # Se tem apenas números, assume que faltam as letras
    elif len(cleaned) == 6 and cleaned.isdigit():
        return cleaned
    
    return cleaned

def is_cpf(idn: str) -> bool:
    return bool(CPF_RE.match(idn))

def is_cnpj(idn: str) -> bool:
    return bool(CNPJ_RE.match(idn))

def is_oab(idn: str) -> bool:
    """Verifica se é uma OAB válida"""
    # Remove caracteres especiais
    cleaned = re.sub(r"[^A-Za-z0-9]", "", idn.upper())
    
    # Verifica se tem 6 números + 2 letras
    if len(cleaned) == 8:
        numbers = cleaned[:6]
        letters = cleaned[6:8]
        return numbers.isdigit() and letters.isalpha()
    
    # Verifica se tem 6 números + 1 letra
    elif len(cleaned) == 7:
        numbers = cleaned[:6]
        letter = cleaned[6]
        return numbers.isdigit() and letter.isalpha()
    
    # Verifica se tem apenas 6 números
    elif len(cleaned) == 6 and cleaned.isdigit():
        return True
    
    return False

def get_oab_command(oab: str) -> str:
    """Gera comando para consulta de OAB"""
    normalized = normalize_oab(oab)
    
    # Se tem apenas números, adiciona /SP como padrão
    if len(normalized) == 6 and normalized.isdigit():
        return f"/oab {normalized}/SP"
    
    # Se já tem formato completo
    if len(normalized) == 8:
        numbers = normalized[:6]
        letters = normalized[6:8]
        return f"/oab {numbers}/{letters}"
    
    # Se tem 7 caracteres
    elif len(normalized) == 7:
        numbers = normalized[:6]
        letter = normalized[6]
        return f"/oab {numbers}/{letter}"
    
    return f"/oab {normalized}"

# ----------------------
# FastAPI Setup
# ----------------------
app = FastAPI()

# Configuração dos templates
templates = Jinja2Templates(directory=TEMPLATES_DIR)

# Configuração dos arquivos estáticos
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# ----------------------
# Consulta no Telegram via Telethon
# ----------------------
@asynccontextmanager
async def get_telegram_client():
    """Context manager para gerenciar conexões do Telethon de forma segura"""
    client = None
    try:
        # Usa lock para evitar conflitos de acesso ao arquivo de sessão
        with telegram_lock:
            client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
            await client.connect()
            
            # Se não estiver autorizado, tenta conectar
            if not await client.is_user_authorized():
                await client.disconnect()
                raise Exception("Cliente Telegram não autorizado. Execute o setup_login.py primeiro.")
                
            yield client
    except Exception as e:
        if client:
            try:
                await client.disconnect()
            except:
                pass
        raise e
    finally:
        if client:
            try:
                await client.disconnect()
            except:
                pass

async def consulta_telegram(cmd: str) -> str:
    """Executa consulta no Telegram com tratamento robusto de erros"""
    try:
        async with get_telegram_client() as client:
            response_text = None
            response_received = asyncio.Event()

            async def handler(event):
                nonlocal response_text
                response_text = re.sub(r"🔛\s*BY:\s*@Skynet08Robot", "", event.raw_text, flags=re.IGNORECASE)
                response_received.set()

            client.add_event_handler(handler, events.NewMessage(chats=GROUP_ID))

            # Envia a mensagem
            await client.send_message(GROUP_ID, cmd)

            # Aguarda resposta com timeout
            try:
                await asyncio.wait_for(response_received.wait(), timeout=30)
                return response_text or "❌ Nenhuma resposta recebida."
            except asyncio.TimeoutError:
                return "❌ Timeout aguardando resposta do bot."
                
    except sqlite3.OperationalError as e:
        if "database is locked" in str(e):
            return "❌ Erro: Banco de dados bloqueado. Tente novamente em alguns segundos."
        else:
            return f"❌ Erro de banco de dados: {str(e)}"
    except Exception as e:
        return f"❌ Erro na consulta: {str(e)}"

# ----------------------
# Rotas
# ----------------------
@app.get("/", response_class=HTMLResponse)
def form(request: Request):
    reuse_value = request.cookies.get("reuse_value") or ""
    return templates.TemplateResponse("modern-form.html", {
        "request": request, 
        "reuse_value": reuse_value
    })

@app.post("/consulta", response_class=HTMLResponse)
async def do_consulta(request: Request):
    form_data = await request.form()
    identificador = str(form_data.get("identificador", ""))
    tipo_consulta = str(form_data.get("tipo_consulta", "cpf_cnpj"))
    
    if not identificador:
        return templates.TemplateResponse(
            "modern-form.html",
            {"request": request, "erro": "Campo identificador é obrigatório.", "reuse_value": identificador}
        )
    
    # Processa baseado no tipo de consulta
    if tipo_consulta == "oab":
        # Consulta OAB
        oab_normalized = normalize_oab(identificador)
        if not is_oab(oab_normalized):
            return templates.TemplateResponse(
                "modern-form.html",
                {"request": request, "erro": "OAB inválida. Use formato: 123456/SP ou 123456SP", "reuse_value": identificador}
            )
        cmd = get_oab_command(oab_normalized)
        tipo_consulta_str = "OAB"
    else:
        # Consulta CPF/CNPJ
        idn = normalize(identificador)
        if is_cpf(idn):
            cmd = f"/cpf3 {idn}"
            tipo_consulta_str = "CPF"
        elif is_cnpj(idn):
            cmd = f"/cnpj {idn}"
            tipo_consulta_str = "CNPJ"
        else:
            return templates.TemplateResponse(
                "modern-form.html",
                {"request": request, "erro": "Identificador inválido. Use CPF (11 dígitos), CNPJ (14 dígitos) ou OAB (123456/SP).", "reuse_value": identificador}
            )
    
    resultado = await consulta_telegram(cmd)
    return templates.TemplateResponse(
        "modern-result.html",
        {"request": request, "mensagem": f"Consulta {tipo_consulta_str} para {identificador}", "resultado": resultado, "identifier": identificador}
    )

@app.get("/historico", response_class=HTMLResponse)
def historico(request: Request):
    return templates.TemplateResponse("historico.html", {"request": request})

@app.get("/limpar-historico", response_class=HTMLResponse)
def limpar_historico(request: Request):
    cursor.execute("DELETE FROM searches")
    conn.commit()
    return templates.TemplateResponse("modern-form.html", {"request": request})


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app:app", host="0.0.0.0", port=port)


