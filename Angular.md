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
- [Notas del Setup](#-notas-del-setup)
- [TODO](#-todo)

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

ng new angular-project

✔ Which stylesheet system would you like to use? Sass (SCSS)     [ https://sass-lang.com/documentation/syntax#scss                ]
✔ Do you want to enable Server-Side Rendering (SSR) and Static Site Generation (SSG/Prerendering)? Yes
✔ Which AI tools do you want to configure with Angular best practices? https://angular.dev/ai/develop-with-ai None
CREATE files created list...
⠴ Installing packages (npm)...

cd <nombre-del-proyecto>

ls

angular.json       package-lock.json  public             src                tsconfig.json
node_modules       package.json       README.md          tsconfig.app.json  tsconfig.spec.json
```

> **Opciones recomendadas durante la creación:**
> - Stylesheet format: `SCSS`
> - SSR (Server-Side Rendering): según necesidad del proyecto

---

## 📦 Dependencias Esenciales

### Angular Material (UI Components)

```bash
ng add @angular/material

✔ Determining Package Manager
  › Using package manager: npm
✔ Searching for compatible package version
  › Found compatible package version: 21.2.2.
✔ Loading package information
✔ Confirming installation
✔ Installing package
✔ Select a pair of starter prebuilt color palettes for your Angular Material theme Rose/Red           [Preview: 
https://material.angular.dev?theme=rose-red]
UPDATE package.json (1101 bytes)
✔ Packages installed successfully.
UPDATE src/styles.scss (1257 bytes)
UPDATE src/index.html (633 bytes)

```

### Animaciones

```bash
npm install @angular/animations

added 1 package, and audited 490 packages in 869ms

109 packages are looking for funding
  run `npm fund` for details

2 high severity vulnerabilities

To address all issues (including breaking changes), run:
  npm audit fix --force

Run `npm audit` for details.
```

### Variables de Entorno

```bash
ng generate environments

ng generate environments
CREATE src/environments/environment.ts (31 bytes)
CREATE src/environments/environment.development.ts (31 bytes)
UPDATE angular.json (2514 bytes)
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
ng g interface core/models/example --type=model
ng g service core/services/api
ng g service core/services/auth
ng g interceptor core/services/http-interceptor
ng g guard core/services/auth-guard

# Resultado esperado:

ng g interface core/models/example --type=model

CREATE src/app/core/models/example.model.ts (29 bytes)

ng g service core/services/api

CREATE src/app/core/services/api.spec.ts (306 bytes)
CREATE src/app/core/services/api.ts (108 bytes)

ng g service core/services/auth

CREATE src/app/core/services/auth.spec.ts (311 bytes)
CREATE src/app/core/services/auth.ts (109 bytes)

ng g interceptor core/services/http-interceptor

CREATE src/app/core/services/http-interceptor-interceptor.spec.ts (521 bytes)
CREATE src/app/core/services/http-interceptor-interceptor.ts (160 bytes)

ng g guard core/services/auth-guard

✔ Which type of guard would you like to create? CanActivate
CREATE src/app/core/services/auth-guard-guard.spec.ts (482 bytes)
CREATE src/app/core/services/auth-guard-guard.ts (133 bytes)
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

Edita `src/app/app.ts` para importar los componentes de Header y Footer:

```typescript 
import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { Footer } from './shared/ui/footer/footer';
import { Header } from './shared/ui/header/header';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, Header, Footer],
  templateUrl: './app.html',
  styleUrl: './app.scss'
})
export class App {
  protected readonly title = signal('angular-project');
}
```

Edita `src/app/app.html` para definir el layout principal:

```html
<app-header />
<main>
  <router-outlet />
</main>
<app-footer />
```

Y en `src/app/app.scss`:

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
      import('./features/home/home').then(m => m.Home),
  },
  {
    path: 'about',
    loadComponent: () =>
      import('./features/about/about').then(m => m.About),
  },
  {
    path: '**',
    loadComponent: () =>
      import('./features/not-found/not-found').then(m => m.NotFound),
  },
];
```

> Se usa **lazy loading** con `loadComponent` para optimizar el rendimiento.

---

## 🔌 Servicios y API

### API Service (`core/services/api.ts`)

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

### `src/environments/environment.development.ts` (Desarrollo)

```typescript
export const environment = {
  production: false,
  apiUrl: 'http://localhost:8000/api',
};
```

---

### `src/environments/environment.ts` (Producción)

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

npx @sentry/wizard@latest -i angular           ✔  system   03:52:14  

┌   Sentry Angular Wizard 
│
◇   ────────────────────────────────────────────────────────────────────────────────────────────────╮
│                                                                                                   │
│  The Sentry Angular Wizard will help you set up Sentry for your application.                      │
│  Thank you for using Sentry :)                                                                    │
│                                                                                                   │
│  Version: 6.12.0                                                                                  │
│                                                                                                   │
│  This wizard sends telemetry data and crash reports to Sentry. This helps us improve the Wizard.  │
│  You can turn this off at any time by running sentry-wizard --disable-telemetry.                  │
│                                                                                                   │
├───────────────────────────────────────────────────────────────────────────────────────────────────╯
│
▲  You have uncommitted or untracked files in your repo:
│  
│  - Angular.md
│  - angular-project/src/app/app.html
│  - angular-project/src/app/app.scss
│  - angular-project/src/app/core/
│  - angular-project/src/app/shared/directives/
│  - angular-project/src/app/shared/pipes/
│  
│  The wizard will create and update files.
│
◇  Do you want to continue anyway?
│  Yes
│
◇  Are you using Sentry SaaS or self-hosted Sentry?
│  Sentry SaaS (sentry.io)
│
◇  Do you already have a Sentry account?
│  Yes
│
●  If the browser window didn't open automatically, please open the following link to log into Sentry:
│  
│  https://sentry.io/account/settings/wizard/d2kohxzqi752ygsb1ibwe7ixnq50jnbv0m91az7immguie1ex2rafogvagwwowg1/?project_platform=javascript-angular
│
◇  Login complete.
│
◇  Selected project hane/node
│
(node:56338) [DEP0190] DeprecationWarning: Passing args to a child process with shell option true can lead to security vulnerabilities, as the arguments are not escaped, only concatenated.
(Use `node --trace-deprecation ...` to show where the warning was created)
◇  Installed @sentry/angular with NPM.
│
◇  Do you want to enable Tracing to track the performance of your application?
│  Yes
│
◇  Do you want to enable Session Replay to get a video-like reproduction of errors during a user session?
│  No
│
◇  Do you want to enable Logs to send your application logs to Sentry?
│  Yes
│
◆  Successfully initialized Sentry in main.ts
│
◆  Successfully updated your app config app.config.ts
│
◇  Installed @sentry/cli@^2 with NPM.
│
◇  Where are your build artifacts located?
│  ./dist
│
◇  We couldn't find build artifacts at "./dist". What would you like to do?
│  Proceed anyway — I believe the path is correct
│
●  Added a sentry:sourcemaps script to your package.json.
│
◇  Do you want to automatically run the sentry:sourcemaps script after each production build?
│  Yes
│
◇  Is npm run build your production build command?
│  Yes
│
●  Added sentry:sourcemaps script to your build command.
│
◆  Added auth token to .sentryclirc for you to test uploading source maps locally.
│
◆  Created .sentryclirc.
│
◆  Added .sentryclirc to .gitignore.
│
◇  Are you using a CI/CD tool to build and deploy your application?
│  Yes
│
◇  Add the Sentry authentication token as an environment variable to your CI setup:

SENTRY_AUTH_TOKEN=
6ImhhbmUifQ=

│
▲  DO NOT commit this auth token to your repository!
│
◇  Did you configure CI as shown above?
│  Yes, continue!
│
◇  Do you want to create an example component to test your Sentry setup?
│  Yes
│
◆  Created example component at ./src/app/sentry-example.component.ts
│
◇  Add the example component one of your pages or components (for example, in app.component.ts).

import { SentryExample } from './sentry-example.component'

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, SentryExample],
  template: `
    <div class="app">
      <h1>Your Application</h1>
      <app-sentry-example></app-sentry-example>
    </div>
  `,
})


│
◇  Did you apply the snippet above?
│  Yes, continue!
│
◇  Looks like you have Prettier in your project. Do you want to run it on your files?
│  Yes
│
◇  Prettier failed to run.
│
▲  Prettier failed to run. There may be formatting issues in your updated files.
│
◇  Optionally add a project-scoped MCP server configuration for the Sentry MCP?
│  No
│
└  Successfully installed the Sentry Angular SDK!

You can validate your setup by starting your dev environment (ng serve) and throwing an error in the example component.

Check out the SDK documentation for further configuration:
https://docs.sentry.io/platforms/javascript/guides/angular/


```

### ESLint

```bash
ng add @angular-eslint/schematics

✔ Determining Package Manager
  › Using package manager: npm
✔ Searching for compatible package version
  › Found compatible package version: 21.3.0.
✔ Loading package information
✔ Confirming installation
✔ Installing package
    
    All angular-eslint dependencies have been successfully installed 🎉
    
    Please see https://github.com/angular-eslint/angular-eslint for how to add ESLint configuration to your project.
    
    We detected that you have a single project in your workspace and no existing linter wired up, so we are configuring ESLint for you automatically.
    
    Please see https://github.com/angular-eslint/angular-eslint for more information.
    
CREATE eslint.config.js (1004 bytes)
UPDATE package.json (1532 bytes)
UPDATE angular.json (2831 bytes)
✔ Packages installed successfully.
```

### Prettier

```bash
npm install --save-dev prettier

up to date, audited 616 packages in 764ms

144 packages are looking for funding
  run `npm fund` for details

2 high severity vulnerabilities

To address all issues (including breaking changes), run:
  npm audit fix --force

Run `npm audit` for details.
```

Crea `.prettierrc`:

```bash
touch .prettierrc
```

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

- [X] Proyecto creado con `ng new`
- [X] Angular Material instalado
- [X] Estructura de carpetas creada
- [X] Routing con lazy loading configurado
- [X] Environments configurados
- [X] Header y Footer implementados
- [X] API Service creado
- [X] HTTP Interceptor configurado
- [X] ESLint + Prettier configurados
- [X] Sentry integrado
- [X] Tests unitarios básicos pasando

---

## 📝 Notas del Setup

> Observaciones relevantes recogidas durante la configuración del boilerplate.

- **Componentes standalone por defecto** — El proyecto fue creado con Angular CLI 21.x, que genera todos los componentes como standalone. No se usa `NgModule` en ningún lugar.
- **`styleUrl` vs `styleUrls`** — El CLI genera `styleUrl` (singular, Angular 17+). Si algún componente necesita múltiples hojas de estilos, usa el array `styleUrls`.
- **Test de humo en `app.spec.ts`** — El test comprueba que `querySelector('p')?.textContent` contenga `'header works!'`, lo que confirma que el `Header` se renderiza correctamente dentro de `app.html`. Si cambias el contenido del header, actualiza también este test.
- **`npm audit`** — Algunos paquetes instalados presentan vulnerabilidades conocidas. Ejecuta `npm audit fix` para las correcciones seguras; las que requieren `--force` pueden introducir breaking changes y deben evaluarse manualmente.
- **Proyecto verificado funcionando** — `npm run start` levanta la aplicación en `localhost:4200` sin errores de compilación ni de consola.

---

## ✅ TODO

> Tareas pendientes identificadas analizando el estado actual de `angular-project/`. Ordenadas por prioridad.

### 🔴 Crítico — El proyecto no funciona correctamente sin esto

- [ ] **Registrar `provideHttpClient()` en `app.config.ts`** — actualmente no está declarado, por lo que cualquier inyección de `HttpClient` lanzará `NullInjectorError` en runtime.
- [ ] **Registrar el interceptor en `app.config.ts`** — `httpInterceptorInterceptor` existe pero nunca se pasa a `withInterceptors([...])`, por lo que no tiene ningún efecto.
- [ ] **Mover `@sentry/cli` a `devDependencies`** — es una herramienta de CI/CD y no debe incluirse en el bundle de producción.

### 🟠 Servicios — Implementar la lógica de negocio

- [ ] **`Api` service** — inyectar `HttpClient` y añadir métodos genéricos (`get`, `post`, `put`, `delete`) con tipado. Leer `environment.apiUrl` como `baseUrl`.
- [ ] **`Auth` service** — implementar gestión de sesión: `login()`, `logout()`, `isAuthenticated()`, almacenamiento seguro del token (no en `localStorage` en producción).
- [ ] **`httpInterceptorInterceptor`** — añadir cabecera `Authorization: Bearer <token>` en cada petición saliente y manejo global de errores HTTP (401 → redirigir a login, 5xx → notificar).
- [ ] **`authGuardGuard`** — hacer que compruebe `Auth.isAuthenticated()` y redirija a `/login` si no está autenticado. Aplicarlo a las rutas protegidas en `app.routes.ts`.

### 🟡 Configuración — Corregir valores por defecto vacíos

- [ ] **`environment.ts` y `environment.development.ts`** — añadir al menos `production: boolean` y `apiUrl: string`. Sin esto, el `ApiService` no tiene base URL.
- [ ] **DSN de Sentry** — reemplazar el DSN placeholder falso por el real del proyecto. Revisar también que `sendDefaultPii: true` sea intencional, ya que envía datos de usuario a Sentry.
- [ ] **Rutas SSR (`app.routes.server.ts`)** — cambiar `RenderMode.Prerender` del wildcard `'**'` a `RenderMode.Server` para evitar pre-renderizado estático del 404.
- [ ] **Eliminar `sentry-example.component.ts`** — el propio comentario del archivo indica que debe borrarse una vez verificado Sentry.

### 🟢 Componentes — Contenido real en lugar de scaffolding

- [ ] **`Header`** — añadir barra de navegación con links a las rutas existentes (`/`, `/about`).
- [ ] **`Footer`** — añadir contenido básico (copyright, links).
- [ ] **`Home`** — implementar contenido real de la página de inicio.
- [ ] **`About`** — implementar contenido real de la página "Acerca de".
- [ ] **`NotFound`** — diseñar página de error 404 y establecer el HTTP status code 404 en SSR mediante `inject(RESPONSE_INIT)`.
- [ ] **`ExamplePipe`** — tipificar correctamente `value` y `args`, implementar la transformación y eliminar el `return null`.
- [ ] **`Example` directive** — implementar lógica real o reemplazar por una directiva útil para el proyecto.
- [ ] **`Example` model** — definir la interfaz con campos reales o eliminarla si no se necesita.

### 🔵 Arquitectura — Buenas prácticas y escalabilidad

- [ ] **Barrel exports (`index.ts`)** — crear archivos `index.ts` en `core/`, `shared/`, y `features/` para simplificar los imports.
- [ ] **Gestión de estado** — evaluar e incorporar un patrón de estado: Signal Store (`@ngrx/signals`), servicios con `signal()`, o `BehaviorSubject`. Actualmente no hay ningún mecanismo.
- [ ] **Manejo de errores y loading** — establecer un patrón consistente para estados de carga y error en los componentes (e.g., `computed()` signals o un `AsyncState<T>` helper).
- [ ] **i18n** — `enableI18nLegacyMessageIdFormat: false` está configurado pero no hay ninguna implementación de internacionalización. Añadir soporte o eliminar la configuración si no se necesita.

### ⚪ Tests — Cobertura real

- [ ] **`ApiService`** — tests con `HttpTestingController` para cada método HTTP.
- [ ] **`AuthService`** — tests de `login()`, `logout()` e `isAuthenticated()`.
- [ ] **`authGuardGuard`** — test de redirección cuando el usuario no está autenticado.
- [ ] **`httpInterceptorInterceptor`** — test que verifica que se añade la cabecera `Authorization`.
- [ ] **`ExamplePipe`** — tests de la transformación con distintos inputs.
- [ ] **Tests de routing** — verificar que las rutas cargan los componentes correctos.
- [ ] **Actualizar `app.spec.ts`** — cuando el `Header` tenga contenido real, actualizar el selector del test para que no dependa del texto placeholder.

### ⚪ CI/CD y Tooling

- [ ] **GitHub Actions** — crear workflow `.github/workflows/ci.yml` con jobs de lint, test y build.
- [ ] **Husky hooks** — verificar que el directorio `.husky/` existe y que el hook `pre-commit` ejecuta `lint-staged`. (Husky está instalado pero los hooks pueden no haberse inicializado.)
- [ ] **`npm audit fix`** — resolver las vulnerabilidades identificadas que no requieran `--force`.

---

> **Hane Boilerplates** — Angular Setup Guide
