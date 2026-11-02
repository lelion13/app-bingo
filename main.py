from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.api import auth, bingo, config_api, users
from app.config import CORS_ORIGINS, IS_PRODUCTION, require_jwt_secret
from app.db import init_db


@asynccontextmanager
async def lifespan(_app: FastAPI):
    require_jwt_secret()
    init_db()
    yield


app = FastAPI(
    lifespan=lifespan,
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

templates = Jinja2Templates(directory="templates")

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(bingo.router)
app.include_router(config_api.router)


@app.get("/health")
async def health():
    return JSONResponse({"status": "ok"})


@app.get("/login", response_class=HTMLResponse)
@app.get("/login/", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse(request, "login.html")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(request, "index.html")


@app.get("/configuracion", response_class=HTMLResponse)
@app.get("/configuracion/", response_class=HTMLResponse)
async def configuracion(request: Request):
    return templates.TemplateResponse(request, "configuracion.html")


@app.get("/usuarios", response_class=HTMLResponse)
@app.get("/usuarios/", response_class=HTMLResponse)
async def usuarios_page(request: Request):
    return templates.TemplateResponse(request, "usuarios.html")


@app.get("/visor/{username}", response_class=HTMLResponse)
@app.get("/visor/{username}/", response_class=HTMLResponse)
async def visor(request: Request, username: str):
    return templates.TemplateResponse(
        request,
        "visor.html",
        context={"username": username.strip().lower()},
    )


@app.get("/visor", response_class=HTMLResponse)
@app.get("/visor/", response_class=HTMLResponse)
async def visor_bare():
    return JSONResponse(
        {"detail": "Usá /visor/<usuario>"},
        status_code=404,
    )


app.mount("/static", StaticFiles(directory="static"), name="static")
