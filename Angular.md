# 🅰️ Angular Boilerplate

> Guía paso a paso para crear un proyecto Angular con buenas prácticas, estructura modular y herramientas esenciales.

---

## 📋 Tabla de Contenidos

- [Requisitos Previos](#-requisitos-previos)
- [Creación del Proyecto](#-creación-del-proyecto)
- [Dependencias Esenciales](#-dependencias-esenciales)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Generación de Componentes](#-generación-de-componentes)
- [Configuración del Layout](#-configuración-del-layout)
- [Routing](#-routing)
- [Servicios y API](#-servicios-y-api)
- [Environments](#-environments)
- [Herramientas Adicionales](#-herramientas-adicionales)
- [Scripts Útiles](#-scripts-útiles)

---

## 🔧 Requisitos Previos

| Herramienta | Versión Mínima | Instalación                      |
| ----------- | -------------- | -------------------------------- |
| Node.js     | 18.x           | [nodejs.org](https://nodejs.org) |
| npm         | 9.x            | Incluido con Node.js             |
| Angular CLI | 19.x           | `npm install -g @angular/cli`    |

Verificar instalación:

```bash
node -v
npm -v
ng version
```

---

## 🚀 Creación del Proyecto

```bash
# Instalar Angular CLI globalmente (si no lo tienes)
npm install -g @angular/cli

# Crear nuevo proyecto
ng new <nombre-del-proyecto>
cd <nombre-del-proyecto>
```

> **Opciones recomendadas durante la creación:**
> - Stylesheet format: `SCSS`
> - SSR (Server-Side Rendering): según necesidad del proyecto

---

## 📦 Dependencias Esenciales

### Angular Material (UI Components)

```bash
ng add @angular/material
```

### Animaciones

```bash
npm install @angular/animations
```

### Variables de Entorno

```bash
ng generate environments
```

---

## 🏗️ Estructura del Proyecto

Esta estructura sigue el patrón **feature-based** (modular), organizando el código en torno a las funcionalidades de la aplicación. Es escalable y facilita el mantenimiento.

```
src/
├── app/
│   ├── core/                          # Singleton services, guards, interceptors
│   │   ├── models/                    # Interfaces y tipos
│   │   │   └── example.model.ts
│   │   ├── services/                  # Servicios globales
│   │   │   ├── api.service.ts         # Comunicación con APIs
│   │   │   ├── auth.service.ts        # Autenticación
│   │   │   ├── interceptor.ts         # HTTP Interceptor
│   │   │   └── guard.ts              # Route Guards
│   │   └── core.module.ts
│   │
│   ├── features/                      # Módulos por funcionalidad
│   │   ├── home/
│   │   │   ├── home.component.ts
│   │   │   ├── home.component.html
│   │   │   ├── home.component.scss
│   │   │   └── home.component.spec.ts
│   │   ├── about/
│   │   │   ├── about.component.ts
│   │   │   ├── about.component.html
│   │   │   ├── about.component.scss
│   │   │   └── about.component.spec.ts
│   │   └── not-found/
│   │       ├── not-found.component.ts
│   │       ├── not-found.component.html
│   │       ├── not-found.component.scss
│   │       └── not-found.component.spec.ts
│   │
│   ├── shared/                        # Componentes, pipes y directivas reutilizables
│   │   ├── ui/
│   │   │   ├── header/
│   │   │   │   ├── header.component.ts
│   │   │   │   ├── header.component.html
│   │   │   │   └── header.component.scss
│   │   │   └── footer/
│   │   │       ├── footer.component.ts
│   │   │       ├── footer.component.html
│   │   │       └── footer.component.scss
│   │   ├── pipes/
│   │   │   └── example.pipe.ts
│   │   └── directives/
│   │       └── example.directive.ts
│   │
│   ├── app.component.ts
│   ├── app.component.html
│   ├── app.component.scss
│   ├── app.config.ts
│   └── app.routes.ts
│
├── assets/
│   └── data/
│       └── data-mock.json             # Datos de prueba
│
├── environments/
│   ├── environment.ts                 # Desarrollo
│   └── environment.prod.ts            # Producción
│
└── styles.scss                        # Estilos globales
```

> **Nota:** Esta estructura es una sugerencia. Puedes adaptarla según las necesidades del proyecto, pero mantener una organización clara es clave para la escalabilidad.

---

## ⚡ Generación de Componentes

Usa Angular CLI para generar los archivos automáticamente con la estructura correcta:

### Features (Páginas)

```bash
ng g c features/home
ng g c features/about
ng g c features/not-found
```

### Shared UI

```bash
ng g c shared/ui/header
ng g c shared/ui/footer
```

### Core (Servicios, Guards, Interceptors)

```bash
ng g class core/models/example --type=model
ng g service core/services/api
ng g service core/services/auth
ng g interceptor core/services/http-interceptor
ng g guard core/services/auth-guard
```

### Shared (Pipes y Directivas)

```bash
ng g pipe shared/pipes/example
ng g directive shared/directives/example
```

### Script completo (copiar y pegar)

```bash
# Features
ng g c features/home && \
ng g c features/about && \
ng g c features/not-found && \

# Shared UI
ng g c shared/ui/header && \
ng g c shared/ui/footer && \

# Core
ng g class core/models/example --type=model && \
ng g service core/services/api && \
ng g service core/services/auth && \
ng g interceptor core/services/http-interceptor && \
ng g guard core/services/auth-guard && \

# Shared
ng g pipe shared/pipes/example && \
ng g directive shared/directives/example
```

---

## 🎨 Configuración del Layout

Edita `src/app/app.component.html` para definir el layout principal:

```html
<app-header />
<main>
  <router-outlet />
</main>
<app-footer />
```

Y en `src/app/app.component.scss`:

```scss
:host {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

main {
  flex: 1;
  padding: 1rem;
}
```

---

## 🛤️ Routing

Configura las rutas en `src/app/app.routes.ts`:

```typescript
import { Routes } from '@angular/router';

export const routes: Routes = [
  {
    path: '',
    loadComponent: () =>
      import('./features/home/home.component').then(m => m.HomeComponent),
  },
  {
    path: 'about',
    loadComponent: () =>
      import('./features/about/about.component').then(m => m.AboutComponent),
  },
  {
    path: '**',
    loadComponent: () =>
      import('./features/not-found/not-found.component').then(m => m.NotFoundComponent),
  },
];
```

> Se usa **lazy loading** con `loadComponent` para optimizar el rendimiento.

---

## 🔌 Servicios y API

### API Service (`core/services/api.service.ts`)

```typescript
import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../../environments/environment';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class ApiService {
  private http = inject(HttpClient);
  private baseUrl = environment.apiUrl;

  get<T>(endpoint: string): Observable<T> {
    return this.http.get<T>(`${this.baseUrl}/${endpoint}`);
  }

  post<T>(endpoint: string, body: unknown): Observable<T> {
    return this.http.post<T>(`${this.baseUrl}/${endpoint}`, body);
  }

  put<T>(endpoint: string, body: unknown): Observable<T> {
    return this.http.put<T>(`${this.baseUrl}/${endpoint}`, body);
  }

  delete<T>(endpoint: string): Observable<T> {
    return this.http.delete<T>(`${this.baseUrl}/${endpoint}`);
  }
}
```

### HTTP Interceptor (`core/services/http-interceptor.ts`)

```typescript
import { HttpInterceptorFn } from '@angular/common/http';

export const httpInterceptor: HttpInterceptorFn = (req, next) => {
  const token = localStorage.getItem('auth_token');

  if (token) {
    const cloned = req.clone({
      setHeaders: {
        Authorization: `Bearer ${token}`,
      },
    });
    return next(cloned);
  }

  return next(req);
};
```

### Registrar el Interceptor en `app.config.ts`

```typescript
import { ApplicationConfig } from '@angular/core';
import { provideRouter } from '@angular/router';
import { provideHttpClient, withInterceptors } from '@angular/common/http';
import { provideAnimationsAsync } from '@angular/platform-browser/animations/async';
import { routes } from './app.routes';
import { httpInterceptor } from './core/services/http-interceptor';

export const appConfig: ApplicationConfig = {
  providers: [
    provideRouter(routes),
    provideHttpClient(withInterceptors([httpInterceptor])),
    provideAnimationsAsync(),
  ],
};
```

---

## 🌍 Environments

### `src/environments/environment.ts` (Desarrollo)

```typescript
export const environment = {
  production: false,
  apiUrl: 'http://localhost:8000/api',
};
```

### `src/environments/environment.prod.ts` (Producción)

```typescript
export const environment = {
  production: true,
  apiUrl: 'https://api.tu-dominio.com/api',
};
```

---

## 🛠️ Herramientas Adicionales

### Sentry (Monitoreo de Errores)

```bash
npx @sentry/wizard@latest -i angular
```

### ESLint

```bash
ng add @angular-eslint/schematics
```

### Prettier

```bash
npm install --save-dev prettier
```

Crea `.prettierrc`:

```json
{
  "singleQuote": true,
  "trailingComma": "all",
  "printWidth": 100,
  "tabWidth": 2,
  "semi": true
}
```

### Husky + lint-staged (Pre-commit hooks)

```bash
npm install --save-dev husky lint-staged
npx husky init
```

---

## 📜 Scripts Útiles

Añade estos scripts a tu `package.json`:

```json
{
  "scripts": {
    "start": "ng serve",
    "build": "ng build",
    "build:prod": "ng build --configuration=production",
    "test": "ng test",
    "test:ci": "ng test --no-watch --code-coverage",
    "lint": "ng lint",
    "format": "prettier --write \"src/**/*.{ts,html,scss}\""
  }
}
```

---

## ✅ Checklist de Setup

- [ ] Proyecto creado con `ng new`
- [ ] Angular Material instalado
- [ ] Estructura de carpetas creada
- [ ] Routing con lazy loading configurado
- [ ] Environments configurados
- [ ] Header y Footer implementados
- [ ] API Service creado
- [ ] HTTP Interceptor configurado
- [ ] ESLint + Prettier configurados
- [ ] Sentry integrado
- [ ] Tests unitarios básicos pasando

---

> **Hane Boilerplates** — Angular Setup Guide
