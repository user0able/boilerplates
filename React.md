# ⚛️ React Boilerplate

> Guía paso a paso para crear un proyecto React con Vite, TypeScript, estructura modular y herramientas esenciales.

---

## 📋 Tabla de Contenidos

- [Requisitos Previos](#-requisitos-previos)
- [Creación del Proyecto](#-creación-del-proyecto)
- [Dependencias Esenciales](#-dependencias-esenciales)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Routing](#-routing)
- [Estado Global](#-estado-global)
- [Fetching de Datos](#-fetching-de-datos)
- [Servicios y API](#-servicios-y-api)
- [Variables de Entorno](#-variables-de-entorno)
- [Estilos](#-estilos)
- [Herramientas de Calidad](#-herramientas-de-calidad)
- [Scripts Útiles](#-scripts-útiles)

---

## 🔧 Requisitos Previos

| Herramienta | Versión Mínima | Instalación |
|-------------|---------------|-------------|
| Node.js     | 18.x          | [nodejs.org](https://nodejs.org) |
| npm         | 9.x           | Incluido con Node.js |

Verificar instalación:

```bash
node -v
npm -v
```

---

## 🚀 Creación del Proyecto

```bash
# Crear proyecto con Vite
npm create vite@latest <nombre-del-proyecto> -- --template react-ts

cd <nombre-del-proyecto>
npm install
```

> **¿Por qué Vite?** Es significativamente más rápido que Create React App (CRA) en desarrollo y build. CRA está deprecado desde 2023.

---

## 📦 Dependencias Esenciales

### Instalación en bloque

```bash
# Routing + Estado + Data fetching
npm install react-router-dom zustand @tanstack/react-query axios

# UI
npm install @mui/material @mui/icons-material @emotion/react @emotion/styled

# Utilidades
npm install clsx
```

### Dev dependencies

```bash
npm install -D @types/node prettier eslint-plugin-react-hooks eslint-plugin-react-refresh
```

---

## 🏗️ Estructura del Proyecto

Estructura **feature-based**, consistente con la usada en el boilerplate de Angular.

```
src/
├── app/                               # Configuración global de la app
│   ├── App.tsx                        # Componente raíz
│   ├── Router.tsx                     # Definición de rutas
│   ├── Providers.tsx                  # Providers (QueryClient, Theme, etc.)
│   └── theme.ts                       # Tema de MUI
│
├── core/                              # Lógica global, singleton
│   ├── api/
│   │   └── api.client.ts             # Cliente HTTP (Axios instance)
│   ├── hooks/
│   │   └── useAuth.ts                # Hook de autenticación
│   ├── models/
│   │   └── user.model.ts             # Interfaces y tipos globales
│   └── stores/
│       └── auth.store.ts             # Store global de autenticación
│
├── features/                          # Módulos por funcionalidad
│   ├── home/
│   │   ├── HomePage.tsx
│   │   ├── components/               # Componentes exclusivos de Home
│   │   │   └── HeroBanner.tsx
│   │   ├── hooks/
│   │   │   └── useHomeData.ts
│   │   └── index.ts                  # Barrel export
│   ├── about/
│   │   ├── AboutPage.tsx
│   │   └── index.ts
│   └── not-found/
│       ├── NotFoundPage.tsx
│       └── index.ts
│
├── shared/                            # Componentes y utilidades reutilizables
│   ├── ui/
│   │   ├── Header/
│   │   │   ├── Header.tsx
│   │   │   └── Header.module.css
│   │   ├── Footer/
│   │   │   ├── Footer.tsx
│   │   │   └── Footer.module.css
│   │   └── Layout/
│   │       └── Layout.tsx
│   ├── components/
│   │   ├── LoadingSpinner.tsx
│   │   └── ErrorBoundary.tsx
│   └── utils/
│       └── format.ts
│
├── assets/
│   └── data/
│       └── data-mock.json
│
├── main.tsx                           # Entry point
└── vite-env.d.ts
```

### Crear la estructura de carpetas

```bash
mkdir -p src/{app,core/{api,hooks,models,stores},features/{home/components,home/hooks,about,not-found},shared/{ui/{Header,Footer,Layout},components,utils},assets/data}
```

---

## 🛤️ Routing

### `src/app/Router.tsx`

```tsx
import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import { lazy, Suspense } from 'react';
import { Layout } from '@/shared/ui/Layout/Layout';

const HomePage = lazy(() => import('@/features/home/HomePage'));
const AboutPage = lazy(() => import('@/features/about/AboutPage'));
const NotFoundPage = lazy(() => import('@/features/not-found/NotFoundPage'));

const router = createBrowserRouter([
  {
    element: <Layout />,
    children: [
      {
        path: '/',
        element: (
          <Suspense fallback={<div>Cargando...</div>}>
            <HomePage />
          </Suspense>
        ),
      },
      {
        path: '/about',
        element: (
          <Suspense fallback={<div>Cargando...</div>}>
            <AboutPage />
          </Suspense>
        ),
      },
      {
        path: '*',
        element: (
          <Suspense fallback={<div>Cargando...</div>}>
            <NotFoundPage />
          </Suspense>
        ),
      },
    ],
  },
]);

export function AppRouter() {
  return <RouterProvider router={router} />;
}
```

> Se usa **lazy loading** con `React.lazy` y `Suspense` para code splitting automático.

### Layout (`src/shared/ui/Layout/Layout.tsx`)

```tsx
import { Outlet } from 'react-router-dom';
import { Header } from '@/shared/ui/Header/Header';
import { Footer } from '@/shared/ui/Footer/Footer';

export function Layout() {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      <Header />
      <main style={{ flex: 1, padding: '1rem' }}>
        <Outlet />
      </main>
      <Footer />
    </div>
  );
}
```

### Configurar Path Aliases

En `vite.config.ts`:

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
});
```

En `tsconfig.json` (dentro de `compilerOptions`):

```json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  }
}
```

---

## 🧠 Estado Global

### Zustand Store (`src/core/stores/auth.store.ts`)

```typescript
import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface User {
  id: string;
  email: string;
  username: string;
}

interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  login: (user: User, token: string) => void;
  logout: () => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      token: null,
      isAuthenticated: false,

      login: (user, token) =>
        set({ user, token, isAuthenticated: true }),

      logout: () =>
        set({ user: null, token: null, isAuthenticated: false }),
    }),
    {
      name: 'auth-storage',
    },
  ),
);
```

> **¿Por qué Zustand?** Mínimo boilerplate, sin providers, TypeScript nativo, y soporta persistencia sin librerías extra.

---

## 🔄 Fetching de Datos

### Configurar TanStack Query (`src/app/Providers.tsx`)

```tsx
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';
import type { ReactNode } from 'react';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000, // 5 minutos
      retry: 1,
      refetchOnWindowFocus: false,
    },
  },
});

interface ProvidersProps {
  children: ReactNode;
}

export function Providers({ children }: ProvidersProps) {
  return (
    <QueryClientProvider client={queryClient}>
      {children}
      <ReactQueryDevtools initialIsOpen={false} />
    </QueryClientProvider>
  );
}
```

### Custom Hook con TanStack Query (`src/features/home/hooks/useHomeData.ts`)

```typescript
import { useQuery } from '@tanstack/react-query';
import { apiClient } from '@/core/api/api.client';

interface HomeData {
  title: string;
  description: string;
}

export function useHomeData() {
  return useQuery<HomeData>({
    queryKey: ['home'],
    queryFn: () => apiClient.get<HomeData>('/home').then((res) => res.data),
  });
}
```

---

## 🔌 Servicios y API

### Cliente HTTP (`src/core/api/api.client.ts`)

```typescript
import axios from 'axios';
import { useAuthStore } from '@/core/stores/auth.store';

export const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor: agregar token a cada request
apiClient.interceptors.request.use((config) => {
  const token = useAuthStore.getState().token;
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Interceptor: manejar errores globales
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      useAuthStore.getState().logout();
      window.location.href = '/login';
    }
    return Promise.reject(error);
  },
);
```

---

## 🌍 Variables de Entorno

### `.env` (Desarrollo)

```env
VITE_API_URL=http://localhost:8000/api
VITE_APP_NAME=Mi App
```

### `.env.production`

```env
VITE_API_URL=https://api.tu-dominio.com/api
VITE_APP_NAME=Mi App
```

> **Nota:** En Vite las variables deben comenzar con `VITE_` para ser accesibles en el cliente. Se acceden con `import.meta.env.VITE_*`.

### Tipado de variables de entorno (`src/vite-env.d.ts`)

```typescript
/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_API_URL: string;
  readonly VITE_APP_NAME: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
```

---

## 🎨 Estilos

### Opción A: CSS Modules (recomendado sin librería extra)

```css
/* src/shared/ui/Header/Header.module.css */
.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem 2rem;
  background-color: #1976d2;
  color: white;
}

.nav {
  display: flex;
  gap: 1rem;
}

.navLink {
  color: white;
  text-decoration: none;
}

.navLink:hover {
  text-decoration: underline;
}
```

```tsx
// src/shared/ui/Header/Header.tsx
import { Link } from 'react-router-dom';
import styles from './Header.module.css';

export function Header() {
  return (
    <header className={styles.header}>
      <h1>Mi App</h1>
      <nav className={styles.nav}>
        <Link to="/" className={styles.navLink}>Inicio</Link>
        <Link to="/about" className={styles.navLink}>Acerca de</Link>
      </nav>
    </header>
  );
}
```

### Opción B: MUI (Material UI)

Ya incluido en las dependencias. Configurar tema en `src/app/theme.ts`:

```typescript
import { createTheme } from '@mui/material/styles';

export const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
  },
  typography: {
    fontFamily: '"Inter", "Roboto", "Helvetica", "Arial", sans-serif',
  },
});
```

Envolver en `Providers.tsx`:

```tsx
import { ThemeProvider, CssBaseline } from '@mui/material';
import { theme } from './theme';

export function Providers({ children }: ProvidersProps) {
  return (
    <QueryClientProvider client={queryClient}>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        {children}
      </ThemeProvider>
      <ReactQueryDevtools initialIsOpen={false} />
    </QueryClientProvider>
  );
}
```

---

## 🧱 Componentes de Página (Ejemplos)

### `src/features/home/HomePage.tsx`

```tsx
export default function HomePage() {
  return (
    <section>
      <h2>Bienvenido</h2>
      <p>Página principal de la aplicación.</p>
    </section>
  );
}
```

### `src/features/about/AboutPage.tsx`

```tsx
export default function AboutPage() {
  return (
    <section>
      <h2>Acerca de</h2>
      <p>Información sobre la aplicación.</p>
    </section>
  );
}
```

### `src/features/not-found/NotFoundPage.tsx`

```tsx
import { Link } from 'react-router-dom';

export default function NotFoundPage() {
  return (
    <section style={{ textAlign: 'center', padding: '4rem' }}>
      <h2>404</h2>
      <p>Página no encontrada.</p>
      <Link to="/">Volver al inicio</Link>
    </section>
  );
}
```

### `src/shared/components/ErrorBoundary.tsx`

```tsx
import { Component, type ReactNode, type ErrorInfo } from 'react';

interface Props {
  children: ReactNode;
  fallback?: ReactNode;
}

interface State {
  hasError: boolean;
}

export class ErrorBoundary extends Component<Props, State> {
  state: State = { hasError: false };

  static getDerivedStateFromError(): State {
    return { hasError: true };
  }

  componentDidCatch(error: Error, info: ErrorInfo) {
    console.error('ErrorBoundary caught:', error, info);
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback ?? <h2>Algo salió mal.</h2>;
    }
    return this.props.children;
  }
}
```

### Entry Point (`src/app/App.tsx`)

```tsx
import { Providers } from './Providers';
import { AppRouter } from './Router';
import { ErrorBoundary } from '@/shared/components/ErrorBoundary';

export function App() {
  return (
    <ErrorBoundary>
      <Providers>
        <AppRouter />
      </Providers>
    </ErrorBoundary>
  );
}
```

### `src/main.tsx`

```tsx
import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { App } from './app/App';

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <App />
  </StrictMode>,
);
```

---

## 🛠️ Herramientas de Calidad

### ESLint (ya incluido con Vite)

Asegúrate de que `eslint.config.js` incluya:

```javascript
import reactHooks from 'eslint-plugin-react-hooks';
import reactRefresh from 'eslint-plugin-react-refresh';

export default [
  // ...configuración base
  {
    plugins: {
      'react-hooks': reactHooks,
      'react-refresh': reactRefresh,
    },
    rules: {
      'react-hooks/rules-of-hooks': 'error',
      'react-hooks/exhaustive-deps': 'warn',
      'react-refresh/only-export-components': ['warn', { allowConstantExport: true }],
    },
  },
];
```

### Prettier

```bash
npm install -D prettier eslint-config-prettier
```

Crea `.prettierrc`:

```json
{
  "singleQuote": true,
  "trailingComma": "all",
  "printWidth": 100,
  "tabWidth": 2,
  "semi": true,
  "jsxSingleQuote": false
}
```

### Husky + lint-staged

```bash
npm install -D husky lint-staged
npx husky init
echo "npx lint-staged" > .husky/pre-commit
```

En `package.json`:

```json
{
  "lint-staged": {
    "*.{ts,tsx}": ["eslint --fix", "prettier --write"],
    "*.{json,md,css}": ["prettier --write"]
  }
}
```

### Vitest (Testing)

```bash
npm install -D vitest @testing-library/react @testing-library/jest-dom jsdom
```

En `vite.config.ts`:

```typescript
/// <reference types="vitest" />
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
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: './src/test/setup.ts',
    css: true,
  },
});
```

Crea `src/test/setup.ts`:

```typescript
import '@testing-library/jest-dom';
```

Ejemplo de test:

```tsx
// src/features/home/HomePage.test.tsx
import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import HomePage from './HomePage';

describe('HomePage', () => {
  it('renders welcome message', () => {
    render(<HomePage />);
    expect(screen.getByText('Bienvenido')).toBeInTheDocument();
  });
});
```

---

## 📜 Scripts Útiles

En `package.json`:

```json
{
  "scripts": {
    "dev": "vite",
    "build": "tsc -b && vite build",
    "preview": "vite preview",
    "test": "vitest",
    "test:run": "vitest run",
    "test:coverage": "vitest run --coverage",
    "lint": "eslint .",
    "lint:fix": "eslint . --fix",
    "format": "prettier --write \"src/**/*.{ts,tsx,css,json}\"",
    "type-check": "tsc --noEmit"
  }
}
```

---

## ✅ Checklist de Setup

- [ ] Proyecto creado con Vite + React + TypeScript
- [ ] Estructura de carpetas feature-based creada
- [ ] Path aliases (`@/`) configurados
- [ ] React Router con lazy loading funcionando
- [ ] Zustand store configurado
- [ ] TanStack Query con cliente Axios
- [ ] Variables de entorno (`.env`) configuradas
- [ ] Layout con Header + Footer
- [ ] Componentes de página básicos (Home, About, 404)
- [ ] ErrorBoundary implementado
- [ ] ESLint + Prettier configurados
- [ ] Husky + lint-staged para pre-commit
- [ ] Vitest + Testing Library configurados
- [ ] Tests básicos pasando

---

> **Hane Boilerplates** — React Setup Guide
