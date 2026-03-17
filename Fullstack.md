# 🔗 Fullstack Boilerplate

> Guía para integrar frontend y backend en un proyecto fullstack unificado con Docker Compose, autenticación compartida y comunicación API. Cubre las combinaciones Angular + Django y React + Node.js/Express.

---

## 📋 Tabla de Contenidos

- [Visión General](#-visión-general)
- [Estructura del Monorepo](#-estructura-del-monorepo)
- [Combo 1: Angular + Django](#-combo-1-angular--django)
- [Combo 2: React + Node.js/Express](#-combo-2-react--nodejsexpress)
- [Docker Compose Unificado](#-docker-compose-unificado)
- [Comunicación Frontend ↔ Backend](#-comunicación-frontend--backend)
- [Autenticación Compartida (JWT)](#-autenticación-compartida-jwt)
- [Proxy en Desarrollo](#-proxy-en-desarrollo)
- [Nginx en Producción](#-nginx-en-producción)
- [Makefile Unificado](#-makefile-unificado)
- [Workflow de Desarrollo](#-workflow-de-desarrollo)

---

## 🎯 Visión General

Un proyecto fullstack combina:

```
┌─────────────┐     HTTP/JSON      ┌─────────────┐      SQL       ┌──────────┐
│  Frontend   │ ◄──────────────── │   Backend   │ ◄────────────► │    DB    │
│ Angular/React│      REST API     │ Django/Node │               │ Postgres │
└─────────────┘                    └─────────────┘               └──────────┘
     :4200/:5173                       :8000/:3000                   :5432
```

Este boilerplate asume que ya tienes configurados los proyectos individuales siguiendo las guías de [Angular.md](Angular.md), [React.md](React.md), [Django.md](Django.md) y [Node.md](Node.md).

---

## 📁 Estructura del Monorepo

### Angular + Django

```
proyecto/
├── frontend/                          # Angular app
│   ├── src/
│   ├── angular.json
│   ├── package.json
│   ├── Dockerfile
│   ├── Dockerfile.dev
│   ├── nginx.conf
│   └── .dockerignore
│
├── backend/                           # Django API
│   ├── apps/
│   ├── config/
│   ├── manage.py
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── Dockerfile.dev
│   └── .dockerignore
│
├── docker-compose.yml                 # Desarrollo
├── docker-compose.prod.yml            # Producción
├── Makefile                           # Comandos unificados
├── .env                               # Variables compartidas
├── .env.example
├── .gitignore
└── README.md
```

### React + Node.js/Express

```
proyecto/
├── frontend/                          # React app (Vite)
│   ├── src/
│   ├── package.json
│   ├── vite.config.ts
│   ├── Dockerfile
│   ├── Dockerfile.dev
│   ├── nginx.conf
│   └── .dockerignore
│
├── backend/                           # Express API
│   ├── src/
│   ├── prisma/
│   ├── package.json
│   ├── tsconfig.json
│   ├── Dockerfile
│   ├── Dockerfile.dev
│   └── .dockerignore
│
├── docker-compose.yml
├── docker-compose.prod.yml
├── Makefile
├── .env
├── .env.example
├── .gitignore
└── README.md
```

### Inicializar el monorepo

```bash
mkdir proyecto && cd proyecto

# Opción A: Angular + Django
ng new frontend --style=scss
mkdir backend && cd backend
python3 -m venv venv && source venv/bin/activate
pip install django djangorestframework
django-admin startproject config .

# Opción B: React + Node.js/Express
npm create vite@latest frontend -- --template react-ts
mkdir backend && cd backend
npm init -y
```

---

## 🅰️🐍 Combo 1: Angular + Django

### `docker-compose.yml`

```yaml
services:
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile.dev
    ports:
      - "4200:4200"
    volumes:
      - ./frontend:/app
      - /app/node_modules
    environment:
      - NODE_ENV=development
    depends_on:
      - backend

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile.dev
    ports:
      - "8000:8000"
    volumes:
      - ./backend:/app
    environment:
      - DJANGO_SETTINGS_MODULE=config.settings.development
      - DATABASE_URL=postgres://postgres:postgres@db:5432/mydb
      - SECRET_KEY=dev-secret-key-change-in-production
      - DEBUG=True
      - ALLOWED_HOSTS=*
      - CORS_ALLOWED_ORIGINS=http://localhost:4200
    depends_on:
      db:
        condition: service_healthy

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

### Proxy de Angular a Django (desarrollo sin CORS)

Crea `frontend/proxy.conf.json`:

```json
{
  "/api": {
    "target": "http://localhost:8000",
    "secure": false,
    "changeOrigin": true
  }
}
```

En `angular.json`, dentro de `serve.options`:

```json
{
  "serve": {
    "options": {
      "proxyConfig": "proxy.conf.json"
    }
  }
}
```

O al arrancar:

```bash
ng serve --proxy-config proxy.conf.json
```

### Configurar Django CORS

En `backend/config/settings/development.py`:

```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:4200",
]
```

### Configurar Angular Environment

En `frontend/src/environments/environment.ts`:

```typescript
export const environment = {
  production: false,
  apiUrl: '/api/v1',  // Usa el proxy en desarrollo
};
```

En `frontend/src/environments/environment.prod.ts`:

```typescript
export const environment = {
  production: true,
  apiUrl: '/api/v1',  // Nginx reverse proxy en producción
};
```

---

## ⚛️🟢 Combo 2: React + Node.js/Express

### `docker-compose.yml`

```yaml
services:
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
      - VITE_API_URL=http://localhost:3000/api/v1
    depends_on:
      - backend

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

### Proxy de Vite a Express (desarrollo)

En `frontend/vite.config.ts`:

```typescript
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:3000',
        changeOrigin: true,
      },
    },
  },
});
```

Con el proxy, el frontend puede hacer requests a `/api/v1/users` y Vite los redirige a `http://localhost:3000/api/v1/users`.

### Backend `.env`

```env
NODE_ENV=development
PORT=3000
DATABASE_URL=postgres://postgres:postgres@db:5432/mydb
JWT_SECRET=dev-secret-key-at-least-32-characters-long
JWT_EXPIRES_IN=30m
CORS_ORIGIN=http://localhost:5173
```

---

## 🔐 Autenticación Compartida (JWT)

El flujo JWT es idéntico para ambas combinaciones:

```
┌──────────┐  POST /auth/login   ┌──────────┐
│ Frontend │ ───────────────────► │ Backend  │
│          │ ◄─────────────────── │          │
│          │   { token, user }    │          │
│          │                      │          │
│          │  GET /api/users      │          │
│          │  Authorization:      │          │
│          │  Bearer <token>      │          │
│          │ ───────────────────► │          │
│          │ ◄─────────────────── │          │
│          │   { data }           │          │
└──────────┘                      └──────────┘
```

### Frontend: Auth Service / Store

#### Angular — `AuthService`

```typescript
import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, tap } from 'rxjs';
import { environment } from '../../../environments/environment';

interface AuthResponse {
  user: { id: string; email: string; username: string };
  token: string;
}

@Injectable({ providedIn: 'root' })
export class AuthService {
  private http = inject(HttpClient);
  private currentUser$ = new BehaviorSubject<AuthResponse['user'] | null>(null);

  user$ = this.currentUser$.asObservable();

  login(email: string, password: string) {
    return this.http
      .post<AuthResponse>(`${environment.apiUrl}/auth/login`, { email, password })
      .pipe(
        tap((res) => {
          localStorage.setItem('auth_token', res.token);
          this.currentUser$.next(res.user);
        }),
      );
  }

  register(data: { email: string; username: string; password: string }) {
    return this.http
      .post<AuthResponse>(`${environment.apiUrl}/auth/register`, data)
      .pipe(
        tap((res) => {
          localStorage.setItem('auth_token', res.token);
          this.currentUser$.next(res.user);
        }),
      );
  }

  logout() {
    localStorage.removeItem('auth_token');
    this.currentUser$.next(null);
  }

  getToken(): string | null {
    return localStorage.getItem('auth_token');
  }
}
```

#### React — Zustand Auth Store

```typescript
import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { apiClient } from '@/core/api/api.client';

interface User {
  id: string;
  email: string;
  username: string;
}

interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (data: { email: string; username: string; password: string }) => Promise<void>;
  logout: () => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      token: null,
      isAuthenticated: false,

      login: async (email, password) => {
        const { data } = await apiClient.post('/auth/login', { email, password });
        set({ user: data.user, token: data.token, isAuthenticated: true });
      },

      register: async (body) => {
        const { data } = await apiClient.post('/auth/register', body);
        set({ user: data.user, token: data.token, isAuthenticated: true });
      },

      logout: () => {
        set({ user: null, token: null, isAuthenticated: false });
      },
    }),
    { name: 'auth-storage' },
  ),
);
```

### Backend: Endpoints de Auth

Los endpoints de autenticación ya están documentados en [Django.md](Django.md) (SimpleJWT) y [Node.md](Node.md) (jsonwebtoken). Resumen de endpoints:

| Método | Endpoint                     | Descripción              |
| ------ | ---------------------------- | ------------------------ |
| POST   | `/api/v1/auth/register`      | Registro de usuario      |
| POST   | `/api/v1/auth/login`         | Login (devuelve JWT)     |
| POST   | `/api/v1/auth/token/refresh` | Refrescar token (Django) |

---

## 🔀 Proxy en Desarrollo

### ¿Por qué usar proxy?

En desarrollo, el frontend y backend corren en puertos diferentes (4200/5173 y 8000/3000). El proxy evita problemas de CORS redirigiendo las llamadas API a través del dev server del frontend.

| Stack        | Archivo de configuración        | Target                  |
| ------------ | ------------------------------- | ----------------------- |
| Angular      | `proxy.conf.json`               | `http://localhost:8000` |
| React (Vite) | `vite.config.ts → server.proxy` | `http://localhost:3000` |

> **Con Docker Compose:** los servicios se comunican por nombre. El frontend container accede al backend como `http://backend:8000` o `http://backend:3000`.

---

## 🌐 Nginx en Producción

En producción, Nginx sirve el frontend estático y actúa como reverse proxy para el backend.

### `nginx.conf` (Producción — Fullstack)

```nginx
upstream backend {
    server backend:8000;    # Django
    # server backend:3000;  # Node.js (descomentar según stack)
}

server {
    listen 80;
    server_name localhost;
    root /usr/share/nginx/html;
    index index.html;

    # Gzip
    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml;
    gzip_min_length 256;

    # API → Backend
    location /api/ {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Admin (Django)
    location /admin/ {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # Static del backend (Django)
    location /static/admin/ {
        proxy_pass http://backend;
    }

    # SPA → index.html
    location / {
        try_files $uri $uri/ /index.html;
    }

    # Cache de assets
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff2?)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

### `docker-compose.prod.yml`

```yaml
services:
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
      target: production
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/conf.d/default.conf:ro
    restart: unless-stopped
    depends_on:
      - backend

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
      target: production
    expose:
      - "8000"          # Solo accesible dentro de la Docker network
    env_file:
      - .env.production
    restart: unless-stopped
    depends_on:
      db:
        condition: service_healthy

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

  redis:
    image: redis:7-alpine
    restart: unless-stopped
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

> En producción, el frontend expone el puerto 80 y Nginx actúa como reverse proxy. El backend usa `expose` (no `ports`) para mantenerse privado dentro de la Docker network.

---

## 🛠️ Makefile Unificado

```makefile
.PHONY: dev prod down logs build migrate seed test lint clean

# ── Desarrollo ──
dev:
	docker compose up --build

dev-d:
	docker compose up -d --build

# ── Producción ──
prod:
	docker compose -f docker-compose.prod.yml up -d --build

# ── Control ──
down:
	docker compose down

down-v:
	docker compose down -v

logs:
	docker compose logs -f

logs-back:
	docker compose logs -f backend

logs-front:
	docker compose logs -f frontend

# ── Build ──
build:
	docker compose build

build-prod:
	docker compose -f docker-compose.prod.yml build

# ── Backend Commands ──
# Django
migrate:
	docker compose exec backend python manage.py migrate

makemigrations:
	docker compose exec backend python manage.py makemigrations

superuser:
	docker compose exec backend python manage.py createsuperuser

shell-django:
	docker compose exec backend python manage.py shell

# Node.js/Express
db-migrate:
	docker compose exec backend npx prisma migrate dev

db-push:
	docker compose exec backend npx prisma db push

db-seed:
	docker compose exec backend npx prisma db seed

db-studio:
	docker compose exec backend npx prisma studio

# ── Frontend Commands ──
fe-install:
	docker compose exec frontend npm install

# ── Testing ──
test-back:
	docker compose exec backend pytest                  # Django
	# docker compose exec backend npm run test:run      # Node

test-front:
	docker compose exec frontend npm run test:run

test:
	$(MAKE) test-back
	$(MAKE) test-front

# ── Linting ──
lint-back:
	docker compose exec backend ruff check .            # Django
	# docker compose exec backend npm run lint          # Node

lint-front:
	docker compose exec frontend npm run lint

lint:
	$(MAKE) lint-back
	$(MAKE) lint-front

# ── Cleanup ──
clean:
	docker compose down -v --rmi local
	docker system prune -f

# ── Setup Inicial ──
setup: dev-d migrate
	@echo ""
	@echo "✅ Proyecto levantado!"
	@echo "   Frontend: http://localhost:4200 (Angular) o http://localhost:5173 (React)"
	@echo "   Backend:  http://localhost:8000 (Django) o http://localhost:3000 (Node)"
	@echo "   DB:       postgres://postgres:postgres@localhost:5432/mydb"
	@echo ""
```

Uso:

```bash
make dev          # Levantar desarrollo
make logs         # Ver logs de todos los servicios
make migrate      # Aplicar migraciones (Django)
make db-migrate   # Aplicar migraciones (Prisma)
make test         # Ejecutar todos los tests
make prod         # Deploy producción
make clean        # Limpiar todo
```

---

## 🔄 Workflow de Desarrollo

### Día a día

```bash
# 1. Levantar el proyecto
make dev

# 2. Abrir en el navegador
#    Frontend: http://localhost:4200 o http://localhost:5173
#    Backend:  http://localhost:8000/api/docs/ o http://localhost:3000/health
#    DB GUI:   npx prisma studio (Node) o localhost:8000/admin/ (Django)

# 3. Editar código → hot reload automático

# 4. Si cambias modelos/schema:
make migrate          # Django
make db-migrate       # Prisma

# 5. Si agregas dependencias:
#    Backend: rebuild container → docker compose up --build backend
#    Frontend: docker compose exec frontend npm install <package>

# 6. Al terminar
make down
```

### Setup desde cero (nuevo desarrollador)

```bash
# 1. Clonar el repo
git clone <repo-url>
cd proyecto

# 2. Copiar variables de entorno
cp .env.example .env
cp backend/.env.example backend/.env

# 3. Levantar todo
make setup

# 4. (Django) Crear superusuario
make superuser

# 5. (Prisma) Seed de datos
make db-seed
```

---

## 📋 Archivos de Entorno

### `.env.example` (raíz del proyecto)

```env
# Database
DB_NAME=mydb
DB_USER=postgres
DB_PASSWORD=postgres

# Shared
NODE_ENV=development
```

### `.env.production` (raíz del proyecto)

```env
# Database
DB_NAME=mydb_prod
DB_USER=app_user
DB_PASSWORD=CHANGE_ME_SECURE_PASSWORD

# Django
DJANGO_SETTINGS_MODULE=config.settings.production
SECRET_KEY=CHANGE_ME_PRODUCTION_SECRET_KEY
ALLOWED_HOSTS=tu-dominio.com,www.tu-dominio.com
CORS_ALLOWED_ORIGINS=https://tu-dominio.com

# Node
NODE_ENV=production
JWT_SECRET=CHANGE_ME_AT_LEAST_32_CHARS_LONG_SECRET

# Sentry
SENTRY_DSN=https://xxxx@sentry.io/yyyy
```

---

## ✅ Checklist de Setup

- [ ] Estructura de monorepo creada (frontend/ + backend/)
- [ ] Frontend configurado siguiendo su guía respectiva
- [ ] Backend configurado siguiendo su guía respectiva
- [ ] Dockerfiles (dev + prod) en cada proyecto
- [ ] `docker-compose.yml` para desarrollo con hot reload
- [ ] `docker-compose.prod.yml` para producción
- [ ] Proxy configurado (Angular proxy.conf.json / Vite server.proxy)
- [ ] CORS configurado en el backend
- [ ] Autenticación JWT compartida (login/register)
- [ ] `nginx.conf` con reverse proxy para producción
- [ ] `Makefile` con comandos unificados
- [ ] Variables de entorno documentadas (`.env.example`)
- [ ] `make dev` levanta todo el stack correctamente
- [ ] Frontend puede hacer requests al backend
- [ ] Tests pasan en ambos proyectos

---

> **Hane Boilerplates** — Fullstack Setup Guide
