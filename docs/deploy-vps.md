# Deploy VPS — bingo.lionapp.cloud

Stack: GHCR + Docker Compose + Traefik (`traefik-wpez`).

## Imagen

- Registry: `ghcr.io/lelion13/app-bingo`
- Repo Git: `https://github.com/lelion13/app-bingo` (tuyo; no el de angel-farina)
- Tags: `latest` (push a `main`), `sha-<corto>`, tags `v*`

Publish automático: `.github/workflows/ghcr.yml` (push a `main` o `workflow_dispatch`).  
El workflow usa `${{ github.repository_owner }}`, así que al estar bajo `lelion13` la imagen sale en `ghcr.io/lelion13/app-bingo`.

Si el paquete GHCR es privado, en el VPS:

```bash
echo TU_GITHUB_TOKEN | docker login ghcr.io -u lelion13 --password-stdin
```

## Primera vez en el VPS

```bash
mkdir -p /docker/app-bingo
cd /docker/app-bingo
# Subir docker-compose.prod.yml y crear .env.prod desde .env.prod.example
cp .env.prod.example .env.prod   # si copiaste el repo; o crearlo a mano
nano .env.prod                   # IMAGE_TAG=latest o sha-...

docker compose --env-file .env.prod -f docker-compose.prod.yml pull
docker compose --env-file .env.prod -f docker-compose.prod.yml up -d
```

DNS: `bingo.lionapp.cloud` → VPS (ya resuelve). Traefik emite TLS con `letsencrypt`.

## Update

```bash
cd /docker/app-bingo
# opcional: fijar IMAGE_TAG=sha-xxxx en .env.prod
docker compose --env-file .env.prod -f docker-compose.prod.yml pull
docker compose --env-file .env.prod -f docker-compose.prod.yml up -d
```

## Verificación

```bash
curl -sS -o /dev/null -w "%{http_code}\n" https://bingo.lionapp.cloud/health   # 200
curl -sS -o /dev/null -w "%{http_code}\n" https://bingo.lionapp.cloud/docs     # 404 en prod
curl -sS -o /dev/null -w "%{http_code}\n" https://bingo.lionapp.cloud/visor    # 200
```

## URLs

| Ruta | Uso |
|------|-----|
| `/` | Consola bingo |
| `/visor` | Solo números (celular/tablet) |
| `/configuracion` | Tiempo/tamaño modal (sesión browser) |
| `/health` | Healthcheck |
