# 🐳 Docker Boilerplate

> Guía completa para containerizar proyectos con Docker y Docker Compose. Incluye Dockerfiles optimizados para Angular, React, Django y Node.js/Express, con configuraciones para desarrollo y producción.

---

## 📋 Tabla de Contenidos

- [Requisitos Previos](#-requisitos-previos)
- [Conceptos Clave](#-conceptos-clave)
- [Angular — Dockerfile](#-angular--dockerfile)
- [React — Dockerfile](#-react--dockerfile)
- [Django — Dockerfile](#-django--dockerfile)
- [Node.js/Express — Dockerfile](#-nodejs-express--dockerfile)
- [Docker Compose — Desarrollo](#-docker-compose--desarrollo)
- [Docker Compose — Producción](#-docker-compose--producción)
- [Comandos Esenciales](#-comandos-esenciales)
- [Volúmenes y Persistencia](#-volúmenes-y-persistencia)
- [Networking](#-networking)
- [Optimización de Imágenes](#-optimización-de-imágenes)
- [Variables de Entorno](#-variables-de-entorno)
- [Troubleshooting](#-troubleshooting)

---

## 🔧 Requisitos Previos

| Herramienta    | Versión Mínima | Instalación |
|----------------|---------------|-------------|
| Docker Engine  | 24.x          | [docker.com](https://docs.docker.com/get-docker/) |
| Docker Compose | 2.20+         | Incluido con Docker Desktop |

Verificar instalación:

```bash
docker --version
docker compose version
```

---

## 📚 Conceptos Clave

| Concepto | Descripción |
|----------|-------------|
| **Image** | Template inmutable con el código y dependencias |
| **Container** | Instancia en ejecución de una imagen |
| **Dockerfile** | Receta para construir una imagen |
| **Compose** | Orquestación de múltiples containers |
| **Volume** | Persistencia de datos fuera del container |
| **Multi-stage build** | Builds en fases para reducir tamaño de imagen |
| **Layer caching** | Reutilización de capas para builds más rápidos |

---

## 🅰️ Angular — Dockerfile

### `Dockerfile` (Multi-stage, Producción)

```dockerfile
# ── Stage 1: Build ──
FROM node:22-alpine AS build

WORKDIR /app

# Copiar package files primero (layer caching)
COPY package.json package-lock.json ./
RUN npm ci

# Copiar código fuente y compilar
COPY . .
RUN npm run build -- --configuration=production

# ── Stage 2: Serve con Nginx ──
FROM nginx:alpine AS production

# Copiar configuración de Nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copiar build artifacts
COPY --from=build /app/dist/*/browser /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

### `nginx.conf` (SPA routing)

```nginx
server {
    listen 80;
    server_name localhost;
    root /usr/share/nginx/html;
    index index.html;

    # Gzip
    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml;
    gzip_min_length 256;

    # SPA: redirigir todas las rutas a index.html
    location / {
        try_files $uri $uri/ /index.html;
    }

    # Cache de assets estáticos
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff2?)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # No cachear index.html
    location = /index.html {
        add_header Cache-Control "no-cache";
    }
}
```

### `Dockerfile.dev` (Desarrollo con hot reload)

```dockerfile
FROM node:22-alpine

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci

COPY . .

EXPOSE 4200

CMD ["npx", "ng", "serve", "--host", "0.0.0.0", "--poll", "2000"]
```

### `.dockerignore`

```
node_modules
dist
.git
.angular
*.md
```

---

## ⚛️ React — Dockerfile

### `Dockerfile` (Multi-stage, Producción)

```dockerfile
# ── Stage 1: Build ──
FROM node:22-alpine AS build

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci

COPY . .
RUN npm run build

# ── Stage 2: Serve con Nginx ──
FROM nginx:alpine AS production

COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

> Reutilizar el mismo `nginx.conf` de Angular (SPA routing idéntico).

### `Dockerfile.dev` (Desarrollo con hot reload)

```dockerfile
FROM node:22-alpine

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci

COPY . .

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
```

### `.dockerignore`

```
node_modules
dist
.git
*.md
```

---

## 🐍 Django — Dockerfile

### `Dockerfile` (Multi-stage, Producción)

```dockerfile
# ── Stage 1: Build dependencies ──
FROM python:3.12-slim AS builder

WORKDIR /app

# Instalar dependencias de compilación
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ── Stage 2: Runtime ──
FROM python:3.12-slim AS production

WORKDIR /app

# Instalar solo runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 && \
    rm -rf /var/lib/apt/lists/*

# Copiar dependencias instaladas
COPY --from=builder /install /usr/local

# Crear usuario no-root
RUN addgroup --system app && adduser --system --ingroup app app

# Copiar código
COPY . .

# Collectstatic
RUN python manage.py collectstatic --noinput 2>/dev/null || true

# Cambiar a usuario no-root
USER app

EXPOSE 8000

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
```

### `Dockerfile.dev` (Desarrollo con auto-reload)

```dockerfile
FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

### `.dockerignore`

```
__pycache__
*.pyc
.git
venv
.env
db.sqlite3
media/
staticfiles/
*.md
```

---

## 🟢 Node.js/Express — Dockerfile

### `Dockerfile` (Multi-stage, Producción)

```dockerfile
# ── Stage 1: Build ──
FROM node:22-alpine AS build

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci

COPY prisma ./prisma
RUN npx prisma generate

COPY . .
RUN npm run build

# ── Stage 2: Production ──
FROM node:22-alpine AS production

WORKDIR /app

# Crear usuario no-root
RUN addgroup -S app && adduser -S app -G app

COPY package.json package-lock.json ./
RUN npm ci --omit=dev

COPY --from=build /app/dist ./dist
COPY --from=build /app/node_modules/.prisma ./node_modules/.prisma
COPY prisma ./prisma

USER app

EXPOSE 3000

CMD ["node", "dist/server.js"]
```

### `Dockerfile.dev` (Desarrollo con watch)

```dockerfile
FROM node:22-alpine

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci

COPY prisma ./prisma
RUN npx prisma generate

COPY . .

EXPOSE 3000

CMD ["npm", "run", "dev"]
```

### `.dockerignore`

```
node_modules
dist
.git
*.md
.env
```

---

## 🐙 Docker Compose — Desarrollo

### `docker-compose.yml` (Angular + Django)

```yaml
services:
  # ── Frontend: Angular ──
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile.dev
    ports:
      - "4200:4200"
    volumes:
      - ./frontend:/app
      - /app/node_modules          # Excluir node_modules del mount
    environment:
      - NODE_ENV=development
    depends_on:
      - backend

  # ── Backend: Django ──
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile.dev
    ports:
      - "8000:8000"
    volumes:
      - ./backend:/app
    env_file:
      - ./backend/.env
    depends_on:
      db:
        condition: service_healthy

  # ── Base de Datos: PostgreSQL ──
  db:
    image: postgres:16-alpine
    ports:
      - "5432:5432"
    environment:
      POSTGRES_DB: mydb
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
```

### `docker-compose.yml` (React + Node.js/Express)

```yaml
services:
  # ── Frontend: React ──
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile.dev
    ports:
      - "5173:5173"
    volumes:
      - ./frontend:/app
      - /app/node_modules
    environment:
      - NODE_ENV=development
    depends_on:
      - backend

  # ── Backend: Node.js/Express ──
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile.dev
    ports:
      - "3000:3000"
    volumes:
      - ./backend:/app
      - /app/node_modules
    env_file:
      - ./backend/.env
    depends_on:
      db:
        condition: service_healthy

  # ── Base de Datos: PostgreSQL ──
  db:
    image: postgres:16-alpine
    ports:
      - "5432:5432"
    environment:
      POSTGRES_DB: mydb
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
```

---

## 🚀 Docker Compose — Producción

### `docker-compose.prod.yml`

```yaml
services:
  # ── Frontend ──
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
      target: production
    ports:
      - "80:80"
    restart: unless-stopped
    depends_on:
      - backend

  # ── Backend ──
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
      target: production
    ports:
      - "8000:8000"
    env_file:
      - ./backend/.env.production
    restart: unless-stopped
    depends_on:
      db:
        condition: service_healthy

  # ── Base de Datos ──
  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: ${DB_NAME}
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${DB_USER}"]
      interval: 10s
      timeout: 5s
      retries: 5

  # ── Redis (Cache/Sessions) ──
  redis:
    image: redis:7-alpine
    restart: unless-stopped
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

Ejecutar producción:

```bash
docker compose -f docker-compose.prod.yml up -d --build
```

---

## ⌨️ Comandos Esenciales

### Lifecycle

```bash
# Levantar servicios en desarrollo
docker compose up

# Levantar en background
docker compose up -d

# Re-construir imágenes
docker compose up --build

# Detener servicios
docker compose down

# Detener y eliminar volúmenes (¡borra datos de BD!)
docker compose down -v

# Ver logs
docker compose logs -f
docker compose logs -f backend     # Solo un servicio

# Ejecutar comando en un container
docker compose exec backend python manage.py migrate
docker compose exec backend npx prisma migrate dev
```

### Imágenes

```bash
# Listar imágenes
docker images

# Eliminar imágenes no usadas
docker image prune

# Build manual de una imagen
docker build -t mi-app:latest .
docker build -t mi-app:latest -f Dockerfile.dev .
```

### Containers

```bash
# Listar containers en ejecución
docker ps

# Listar todos (incluyendo detenidos)
docker ps -a

# Entrar a un container
docker exec -it <container_id> sh

# Ver uso de recursos
docker stats
```

### Limpieza

```bash
# Limpiar todo lo no usado (imágenes, containers, networks, cache)
docker system prune -a

# Solo cache de builds
docker builder prune
```

---

## 💾 Volúmenes y Persistencia

| Tipo | Uso | Sintaxis |
|------|-----|----------|
| **Named volume** | Datos persistentes (BD) | `postgres_data:/var/lib/postgresql/data` |
| **Bind mount** | Código fuente (dev) | `./backend:/app` |
| **Anonymous volume** | Excluir directorios | `/app/node_modules` |

```bash
# Listar volúmenes
docker volume ls

# Inspeccionar volumen
docker volume inspect postgres_data

# Eliminar volúmenes huérfanos
docker volume prune
```

---

## 🌐 Networking

Docker Compose crea una network automática donde los servicios se comunican por nombre:

```
frontend  →  http://backend:8000/api
backend   →  postgres://db:5432/mydb
backend   →  redis://redis:6379
```

```bash
# Ver networks
docker network ls

# Inspeccionar network
docker network inspect <project>_default
```

---

## 📦 Optimización de Imágenes

### Buenas Prácticas

1. **Usar imágenes `alpine`** — 5-10x más ligeras que las completas
2. **Multi-stage builds** — Separar build de runtime
3. **Copiar `package.json` primero** — Aprovechar Docker layer caching
4. **`.dockerignore`** — Excluir archivos innecesarios
5. **`npm ci` sobre `npm install`** — Builds reproducibles y más rápidos
6. **Usuario no-root** — Seguridad en producción

### Comparativa de tamaños

| Base image | Tamaño aprox. |
|-----------|---------------|
| `node:22` | ~1.1 GB |
| `node:22-slim` | ~200 MB |
| `node:22-alpine` | ~130 MB |
| `python:3.12` | ~1.0 GB |
| `python:3.12-slim` | ~150 MB |
| `nginx:alpine` | ~40 MB |

### Resultado final (con multi-stage)

| App | Tamaño imagen |
|-----|--------------|
| Angular (nginx) | ~50 MB |
| React (nginx) | ~45 MB |
| Django (slim) | ~200 MB |
| Node.js (alpine) | ~180 MB |

---

## 🔒 Variables de Entorno

### `.env` para Docker Compose

```env
# Database
DB_NAME=mydb
DB_USER=postgres
DB_PASSWORD=secure_password_here

# App
NODE_ENV=production
DJANGO_SETTINGS_MODULE=config.settings.production
```

> **Seguridad:** Nunca commitees `.env` con credenciales reales. Usa Docker secrets o un gestor de secrets en producción.

---

## 🔍 Troubleshooting

| Problema | Solución |
|----------|----------|
| Hot reload no funciona (Angular/React) | Agregar `--poll 2000` al serve command |
| `node_modules` vacío en container | Usar anonymous volume: `/app/node_modules` |
| Permisos de archivos en Linux | Usar `user: "${UID}:${GID}"` en compose |
| Container se cierra inmediatamente | Revisar logs: `docker compose logs <service>` |
| Puerto ya en uso | Cambiar el puerto en compose o liberar: `lsof -i :<port>` |
| Build lento | Verificar `.dockerignore`, usar layer caching |
| DB no conecta | Esperar healthcheck: `depends_on: condition: service_healthy` |
| "Cannot find module" | El volume mount puede pisar `node_modules`. Usar anonymous volume |

---

## ✅ Checklist de Setup

- [ ] Docker y Docker Compose instalados
- [ ] Dockerfiles creados para cada servicio
- [ ] `.dockerignore` configurado en cada proyecto
- [ ] `docker-compose.yml` para desarrollo con hot reload
- [ ] `docker-compose.prod.yml` para producción
- [ ] Volúmenes para persistencia de BD
- [ ] Health checks en servicios de infraestructura
- [ ] Variables de entorno en `.env` (no commiteadas)
- [ ] Imágenes optimizadas con multi-stage builds
- [ ] Usuarios no-root en producción
- [ ] `nginx.conf` para SPAs (Angular/React)
- [ ] Todos los servicios levantan con `docker compose up`

---

> **Hane Boilerplates** — Docker Setup Guide
