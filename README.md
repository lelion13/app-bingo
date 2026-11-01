# 🎱 Bingo Bolillero 3D (90 Números)

Aplicación web interactiva para jugar al **Bingo de 90 bolillas**, desarrollada con **FastAPI** en el backend y **Three.js** para la visualización 3D en el frontend.

---

## ✨ Características

- **Backend Rápido:** Construido con FastAPI para una gestión eficiente del estado del juego.  
- **Visualización 3D:** Esfera interactiva renderizada con Three.js que gira al sacar una bolilla.  
- **Interfaz Moderna:** Estilizada con Tailwind CSS y animaciones fluidas.  
- **Sonidos y Efectos:** Incluye efectos de sonido de ruleta y confeti al ganar.  
- **Historial en Tiempo Real:** Muestra las últimas bolillas y permite ver todas las que han salido.  
- **Docker Ready:** Listo para desplegar en cualquier entorno de contenedores.

---

## 🚀 Estructura del Proyecto

Asegúrate de tener la siguiente estructura de carpetas para que los archivos estáticos (imágenes, sonidos y scripts) carguen correctamente:

```
/
├── main.py                 # Lógica del servidor FastAPI
├── Dockerfile              # Configuración de la imagen Docker
├── requirements.txt        # Dependencias de Python
├── templates/
│   └── index.html          # Frontend principal
└── static/
    ├── favicon.png         # Icono de la pestaña
    ├── logo.png            # Logo del bingo
    ├── pattern_soccer.jpg  # Textura para la bola 3D
    ├── js/
    │   └── main.js         # Lógica del cliente y Three.js
    └── sounds/
        ├── spinning-roulette-wheel-4s.mp3
        └── cheers_crowd.mp3   # (opcional)
```

---

## 🛠️ Requisitos Previos

- **Docker** (recomendado), o  
- **Python 3.11+** instalado localmente.

---

## 📦 Instalación y Uso

### Opción A: Usando Docker (Recomendada)

**1. Construir la imagen:**
```bash
docker build -t bingo-app .
```

**2. Correr el contenedor:**
```bash
docker run -d -p 8000:8000 --name mi-bingo bingo-app
```

**3. Abrir en el navegador:**
```
http://localhost:8000
```

---

### Opción B: Ejecución Local (Python)

**1. Crear entorno virtual:**
```bash
python -m venv venv
source venv/bin/activate   # En Windows: venv\Scripts\activate
```

**2. Instalar dependencias:**
```bash
pip install -r requirements.txt
```

**3. Ejecutar el servidor:**
```bash
uvicorn main:app --reload
```

---

## 🔧 Tecnologías Utilizadas

- **Backend:** Python, FastAPI, Jinja2 Templates  
- **Frontend:** HTML5, JavaScript (ES6+)  
- **Gráficos 3D:** Three.js  
- **Estilos:** Tailwind CSS (vía CDN), Bootstrap 5 (para Toasts y Modales)  
- **Efectos:** Canvas Confetti  

---

## 📄 API Endpoints

| Método | Endpoint            | Descripción |
|---------|---------------------|--------------|
| `GET`   | `/`                 | Renderiza la interfaz del juego |
| `GET`   | `/iniciar_bingo/`   | Reinicia el juego y mezcla las bolillas |
| `GET`   | `/sacar_bolilla/`   | Extrae una bolilla aleatoria y actualiza el estado |
| `GET`   | `/estado/`          | Devuelve el JSON con las bolillas restantes y las que salieron |

---

## ☁️ Producción (GHCR + Traefik)

- Dominio: `https://bingo.lionapp.cloud`
- Repo: `https://github.com/lelion13/app-bingo`
- Imagen: `ghcr.io/lelion13/app-bingo`
- Compose: `docker-compose.prod.yml`
- Guía VPS: [`docs/deploy-vps.md`](docs/deploy-vps.md)

Desarrollado con ❤️
