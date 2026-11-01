import os
import random

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

APP_ENV = os.getenv("APP_ENV", "development").lower()
IS_PRODUCTION = APP_ENV in ("production", "prod")

_cors_raw = os.getenv("CORS_ORIGINS", "*").strip()
CORS_ORIGINS = (
    ["*"]
    if _cors_raw == "*"
    else [origin.strip() for origin in _cors_raw.split(",") if origin.strip()]
)

app = FastAPI(
    docs_url=None if IS_PRODUCTION else "/docs",
    redoc_url=None if IS_PRODUCTION else "/redoc",
    openapi_url=None if IS_PRODUCTION else "/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# rutas estáticas y plantillas
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Estado del bingo
bolillas_disponibles = list(range(1, 91))  # Bingo de 90 números
random.shuffle(bolillas_disponibles)
bolillas_salidas = []

@app.get("/health")
async def health():
    return JSONResponse({"status": "ok"})

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )

@app.get("/configuracion", response_class=HTMLResponse)
@app.get("/configuracion/", response_class=HTMLResponse)
async def configuracion(request: Request):
    return templates.TemplateResponse(
        "configuracion.html",
        {"request": request}
    )

@app.get("/visor", response_class=HTMLResponse)
@app.get("/visor/", response_class=HTMLResponse)
async def visor(request: Request):
    """Pantalla solo-lectura para celular/tablet con números salidos."""
    return templates.TemplateResponse(
        "visor.html",
        {"request": request}
    )

@app.get("/iniciar_bingo/")
async def iniciar_bingo():
    """Reinicia el juego con todas las bolillas disponibles"""
    global bolillas_disponibles, bolillas_salidas
    bolillas_disponibles = list(range(1, 91))
    bolillas_salidas = []
    random.shuffle(bolillas_disponibles)
    return JSONResponse({
        "mensaje": "✅ Bingo (90) iniciado",
        "total": len(bolillas_disponibles)
    })

@app.get("/sacar_bolilla/")
async def sacar_bolilla():
    """Saca una bolilla al azar"""
    global bolillas_disponibles, bolillas_salidas
    
    if not bolillas_disponibles:
        return JSONResponse({
            "error": "No quedan más bolillas",
            "mensaje": "🎊 ¡Bingo completo!"
        })
    
    bolilla = bolillas_disponibles.pop(0)
    bolillas_salidas.append(bolilla)
    
    return JSONResponse({
        "bolilla": bolilla,
        "restantes": len(bolillas_disponibles),
        "salidas": bolillas_salidas
    })

@app.get("/estado/")
async def obtener_estado():
    """Obtiene el estado actual del bingo"""
    return JSONResponse({
        "restantes": len(bolillas_disponibles),
        "salidas": bolillas_salidas,
        "total": 90
    })