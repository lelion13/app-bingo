# Deploy VPS — bingo.lionapp.cloud

Stack: GHCR + Docker Compose + Traefik (`traefik-wpez`) + SQLite (volumen) + JWT.

## Imagen

- Registry: `ghcr.io/lelion13/app-bingo`
- Repo Git: `https://github.com/lelion13/app-bingo`
- Tags: `latest` (push a `main`), `sha-<corto>`, tags `v*`

Publish automático: `.github/workflows/ghcr.yml`.

Si el paquete GHCR es privado, en el VPS:

```bash
echo TU_GITHUB_TOKEN | docker login ghcr.io -u lelion13 --password-stdin
```

## Primera vez en el VPS

```bash
mkdir -p /docker/app-bingo
cd /docker/app-bingo
# Subir docker-compose.prod.yml y crear .env.prod desde .env.prod.example
cp .env.prod.example .env.prod
nano .env.prod                   # IMAGE_TAG, JWT_SECRET (obligatorio)

docker compose --env-file .env.prod -f docker-compose.prod.yml pull
docker compose --env-file .env.prod -f docker-compose.prod.yml up -d
```

### Bootstrap del primer admin

Con el contenedor corriendo (volumen `bingo-data` montado en `/data`):

```bash
docker compose --env-file .env.prod -f docker-compose.prod.yml exec bingo \
  python scripts/bootstrap_admin.py --username admin --password 'TU_CLAVE_SEGURA'
```

El script falla si ya existe un admin. Luego creá operadores desde `/usuarios` (logueado como admin).

DNS: `bingo.lionapp.cloud` → VPS. Traefik emite TLS con `letsencrypt`.

## Update

```bash
cd /docker/app-bingo
docker compose --env-file .env.prod -f docker-compose.prod.yml pull
docker compose --env-file .env.prod -f docker-compose.prod.yml up -d
```

El volumen SQLite se conserva entre recreaciones del contenedor.

## Verificación

```bash
curl -sS -o /dev/null -w "%{http_code}\n" https://bingo.lionapp.cloud/health          # 200
curl -sS -o /dev/null -w "%{http_code}\n" https://bingo.lionapp.cloud/docs            # 404 en prod
curl -sS -o /dev/null -w "%{http_code}\n" https://bingo.lionapp.cloud/visor           # 404 (usar /visor/<usuario>)
curl -sS -o /dev/null -w "%{http_code}\n" https://bingo.lionapp.cloud/visor/admin     # 200 si existe admin
```

## URLs

| Ruta | Uso |
|------|-----|
| `/login` | Ingreso (JWT) |
| `/` | Consola bingo (JWT) |
| `/usuarios` | ABM usuarios (solo admin) |
| `/visor/<usuario>` | Visor público solo lectura |
| `/configuracion` | Modal duration/tamaño (por usuario, SQLite) |
| `/health` | Healthcheck |

## Variables

| Variable | Notas |
|----------|--------|
| `JWT_SECRET` | Obligatorio en prod |
| `DATABASE_PATH` | Default `/data/bingo.db` (volumen) |
| `APP_ENV` | `production` desactiva `/docs` |
| `CORS_ORIGINS` | Origen front si aplica |
