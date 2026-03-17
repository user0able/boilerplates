# 🖖 Vue.js Boilerplate

> Guía paso a paso para crear un proyecto Vue 3 con Vite, TypeScript, estructura modular y herramientas esenciales.

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
- [Composables](#-composables)
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
npm create vite@latest <nombre-del-proyecto> -- --template vue-ts

cd <nombre-del-proyecto>
npm install
```

> **¿Por qué Vite?** El tooling oficial de Vue 3 (create-vue) también usa Vite internamente. Vite ofrece HMR instantáneo y builds optimizados.

Alternativa con `create-vue` (instalador oficial con más opciones):

```bash
npm create vue@latest
```

> `create-vue` permite activar Vue Router, Pinia, Vitest, ESLint y Prettier desde el wizard de creación.

---

## 📦 Dependencias Esenciales

### Routing + Estado + Data fetching

```bash
npm install vue-router pinia @tanstack/vue-query axios
```

### UI

```bash
# Opción A: Vuetify (Material Design)
npm install vuetify @mdi/font

# Opción B: PrimeVue
npm install primevue @primevue/themes

# Opción C: Headless UI + Tailwind
npm install -D tailwindcss autoprefixer postcss
npx tailwindcss init -p
```

### Utilidades

```bash
npm install @vueuse/core
```

> **VueUse** es una colección de composables esenciales (equivalente a los hooks de React): `useLocalStorage`, `useFetch`, `useDebounce`, `useEventListener`, etc.

### Dev dependencies

```bash
npm install -D @types/node
```

---

## 🏗️ Estructura del Proyecto

Estructura **feature-based**, consistente con los otros boilerplates de esta colección.

```
src/
├── app/                               # Configuración global de la app
│   ├── App.vue                        # Componente raíz
│   └── plugins/                       # Registro de plugins (Vuetify, etc.)
│       ├── index.ts                   # Registra todos los plugins
│       └── vuetify.ts                 # Configuración de Vuetify
│
├── core/                              # Lógica global, singleton
│   ├── api/
│   │   └── api.client.ts             # Cliente HTTP (Axios instance)
│   ├── composables/
│   │   └── useAuth.ts                # Composable de autenticación
│   ├── models/
│   │   └── user.model.ts             # Interfaces y tipos globales
│   └── stores/
│       └── auth.store.ts             # Pinia store de autenticación
│
├── features/                          # Módulos por funcionalidad
│   ├── home/
│   │   ├── HomePage.vue
│   │   ├── components/               # Componentes exclusivos de Home
│   │   │   └── HeroBanner.vue
│   │   ├── composables/
│   │   │   └── useHomeData.ts
│   │   └── index.ts                  # Barrel export
│   ├── about/
│   │   ├── AboutPage.vue
│   │   └── index.ts
│   └── not-found/
│       ├── NotFoundPage.vue
│       └── index.ts
│
├── shared/                            # Componentes y utilidades reutilizables
│   ├── ui/
│   │   ├── TheHeader.vue
│   │   ├── TheFooter.vue
│   │   └── BaseLayout.vue
│   ├── components/
│   │   └── BaseButton.vue
│   └── utils/
│       └── format.ts
│
├── assets/
│   └── data/
│       └── data-mock.json
│
├── main.ts                            # Entry point
├── router.ts                          # Definición de rutas
└── env.d.ts                           # Tipado de variables de entorno
```

### Crear la estructura de carpetas

```bash
mkdir -p src/{app/plugins,core/{api,composables,models,stores},features/{home/components,home/composables,about,not-found},shared/{ui,components,utils},assets/data}
```

---

## 🛤️ Routing

### `src/router.ts`

```typescript
import { createRouter, createWebHistory } from 'vue-router';
import { useAuthStore } from '@/core/stores/auth.store';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      component: () => import('@/features/home/HomePage.vue'),
    },
    {
      path: '/about',
      component: () => import('@/features/about/AboutPage.vue'),
    },
    {
      path: '/login',
      component: () => import('@/features/auth/LoginPage.vue'),
      meta: { requiresGuest: true },
    },
    {
      path: '/dashboard',
      component: () => import('@/features/dashboard/DashboardPage.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/:pathMatch(.*)*',
      component: () => import('@/features/not-found/NotFoundPage.vue'),
    },
  ],
});

// Navigation Guard
router.beforeEach((to) => {
  const auth = useAuthStore();

  if (to.meta.requiresAuth && !auth.isAuthenticated) {
    return '/login';
  }
  if (to.meta.requiresGuest && auth.isAuthenticated) {
    return '/';
  }
});

export default router;
```

> Vue Router usa **dynamic imports** automáticamente con la sintaxis `() => import(...)`, habilitando code splitting.

### Layout (`src/shared/ui/BaseLayout.vue`)

```vue
<script setup lang="ts">
import TheHeader from './TheHeader.vue';
import TheFooter from './TheFooter.vue';
</script>

<template>
  <div class="layout">
    <TheHeader />
    <main class="layout__main">
      <RouterView />
    </main>
    <TheFooter />
  </div>
</template>

<style scoped>
.layout {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.layout__main {
  flex: 1;
  padding: 1rem;
}
</style>
```

### `src/app/App.vue`

```vue
<script setup lang="ts">
import BaseLayout from '@/shared/ui/BaseLayout.vue';
</script>

<template>
  <BaseLayout />
</template>
```

### Configurar Path Aliases

En `vite.config.ts`:

```typescript
import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import path from 'path';

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
});
```

En `tsconfig.json`:

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

### Pinia Store (`src/core/stores/auth.store.ts`)

```typescript
import { defineStore } from 'pinia';
import { ref, computed } from 'vue';

interface User {
  id: string;
  email: string;
  username: string;
}

export const useAuthStore = defineStore(
  'auth',
  () => {
    // State
    const user = ref<User | null>(null);
    const token = ref<string | null>(null);

    // Getters
    const isAuthenticated = computed(() => !!token.value);

    // Actions
    function login(newUser: User, newToken: string) {
      user.value = newUser;
      token.value = newToken;
    }

    function logout() {
      user.value = null;
      token.value = null;
    }

    return { user, token, isAuthenticated, login, logout };
  },
  {
    persist: true, // Requiere pinia-plugin-persistedstate
  },
);
```

### Persistencia del Store

```bash
npm install pinia-plugin-persistedstate
```

Registrar en `src/main.ts`:

```typescript
import { createPinia } from 'pinia';
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate';

const pinia = createPinia();
pinia.use(piniaPluginPersistedstate);
```

> **¿Por qué Pinia?** Es el gestor de estado oficial para Vue 3. Reemplaza a Vuex. TypeScript nativo, sin mutations, Composition API friendly y DevTools integradas.

---

## 🔄 Fetching de Datos

### Configurar TanStack Query (`src/main.ts`)

```typescript
import { VueQueryPlugin, QueryClient } from '@tanstack/vue-query';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000, // 5 minutos
      retry: 1,
      refetchOnWindowFocus: false,
    },
  },
});

app.use(VueQueryPlugin, { queryClient });
```

### Composable con TanStack Query (`src/features/home/composables/useHomeData.ts`)

```typescript
import { useQuery } from '@tanstack/vue-query';
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

Uso en un componente:

```vue
<script setup lang="ts">
import { useHomeData } from './composables/useHomeData';

const { data, isLoading, isError } = useHomeData();
</script>

<template>
  <div>
    <p v-if="isLoading">Cargando...</p>
    <p v-else-if="isError">Error al cargar datos.</p>
    <h1 v-else>{{ data?.title }}</h1>
  </div>
</template>
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
  const auth = useAuthStore();
  if (auth.token) {
    config.headers.Authorization = `Bearer ${auth.token}`;
  }
  return config;
});

// Interceptor: manejar errores globales
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      const auth = useAuthStore();
      auth.logout();
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
VITE_APP_NAME=Mi App Vue
```

### `.env.production`

```env
VITE_API_URL=https://api.tu-dominio.com/api
VITE_APP_NAME=Mi App Vue
```

> En Vite las variables deben comenzar con `VITE_` para ser accesibles en el cliente.

### Tipar variables de entorno (`src/env.d.ts`)

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

### Opción A: Scoped CSS (por defecto, sin dependencias)

```vue
<style scoped>
/* Solo aplica a este componente */
.header {
  display: flex;
  align-items: center;
  padding: 1rem 2rem;
  background-color: #1867c0;
  color: white;
}
</style>
```

### Opción B: Vuetify (Material Design)

```bash
npm install vuetify @mdi/font
```

Crea `src/app/plugins/vuetify.ts`:

```typescript
import 'vuetify/styles';
import '@mdi/font/css/materialdesignicons.css';
import { createVuetify } from 'vuetify';
import * as components from 'vuetify/components';
import * as directives from 'vuetify/directives';

export default createVuetify({
  components,
  directives,
  theme: {
    defaultTheme: 'light',
    themes: {
      light: {
        colors: {
          primary: '#1867c0',
          secondary: '#5cbbf6',
        },
      },
    },
  },
});
```

Registrar en `src/main.ts`:

```typescript
import vuetify from './app/plugins/vuetify';
app.use(vuetify);
```

### Opción C: Tailwind CSS

```bash
npm install -D tailwindcss autoprefixer postcss
npx tailwindcss init -p
```

`tailwind.config.js`:

```javascript
export default {
  content: ['./index.html', './src/**/*.{vue,js,ts}'],
  theme: {
    extend: {},
  },
  plugins: [],
};
```

Importar en `src/assets/main.css`:

```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

---

## 🧩 Composables

Los composables son el equivalente Vue a los React Hooks. Usan la Composition API para encapsular lógica reutilizable.

### `src/core/composables/useAuth.ts`

```typescript
import { computed } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/core/stores/auth.store';
import { apiClient } from '@/core/api/api.client';

export function useAuth() {
  const auth = useAuthStore();
  const router = useRouter();

  const isAuthenticated = computed(() => auth.isAuthenticated);

  async function login(email: string, password: string) {
    const { data } = await apiClient.post('/auth/login', { email, password });
    auth.login(data.user, data.token);
    await router.push('/dashboard');
  }

  async function register(payload: { email: string; username: string; password: string }) {
    const { data } = await apiClient.post('/auth/register', payload);
    auth.login(data.user, data.token);
    await router.push('/dashboard');
  }

  function logout() {
    auth.logout();
    router.push('/login');
  }

  return { isAuthenticated, login, register, logout };
}
```

### `src/shared/ui/TheHeader.vue`

```vue
<script setup lang="ts">
import { RouterLink } from 'vue-router';
import { useAuth } from '@/core/composables/useAuth';

const { isAuthenticated, logout } = useAuth();
</script>

<template>
  <header class="header">
    <RouterLink to="/" class="logo">Mi App</RouterLink>
    <nav>
      <RouterLink to="/">Inicio</RouterLink>
      <RouterLink to="/about">Acerca de</RouterLink>
      <template v-if="isAuthenticated">
        <RouterLink to="/dashboard">Dashboard</RouterLink>
        <button @click="logout">Salir</button>
      </template>
      <RouterLink v-else to="/login">Iniciar sesión</RouterLink>
    </nav>
  </header>
</template>

<style scoped>
.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem 2rem;
  background-color: #1867c0;
  color: white;
}

.header nav {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.header a {
  color: white;
  text-decoration: none;
}

.header a:hover,
.header a.router-link-active {
  text-decoration: underline;
}

.header button {
  background: none;
  border: 1px solid white;
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 4px;
  cursor: pointer;
}
</style>
```

---

## 🧱 Componentes de Página (Ejemplos)

### `src/features/home/HomePage.vue`

```vue
<script setup lang="ts">
import { useHomeData } from './composables/useHomeData';

const { data, isLoading } = useHomeData();
</script>

<template>
  <section>
    <h2>Bienvenido</h2>
    <p v-if="isLoading">Cargando...</p>
    <p v-else>{{ data?.description ?? 'Página principal de la aplicación.' }}</p>
  </section>
</template>
```

### `src/features/about/AboutPage.vue`

```vue
<template>
  <section>
    <h2>Acerca de</h2>
    <p>Información sobre la aplicación.</p>
  </section>
</template>
```

### `src/features/not-found/NotFoundPage.vue`

```vue
<template>
  <section style="text-align: center; padding: 4rem">
    <h2>404</h2>
    <p>Página no encontrada.</p>
    <RouterLink to="/">Volver al inicio</RouterLink>
  </section>
</template>
```

---

## 🚀 Entry Point

### `src/main.ts`

```typescript
import { createApp } from 'vue';
import { createPinia } from 'pinia';
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate';
import { VueQueryPlugin, QueryClient } from '@tanstack/vue-query';
import router from './router';
import App from './app/App.vue';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000,
      retry: 1,
      refetchOnWindowFocus: false,
    },
  },
});

const pinia = createPinia();
pinia.use(piniaPluginPersistedstate);

const app = createApp(App);

app.use(pinia);
app.use(router);
app.use(VueQueryPlugin, { queryClient });

app.mount('#app');
```

---

## 🛠️ Herramientas de Calidad

### ESLint + Vue Plugin

```bash
npm install -D eslint @eslint/js typescript-eslint eslint-plugin-vue vue-eslint-parser eslint-config-prettier prettier
```

`eslint.config.js`:

```javascript
import eslint from '@eslint/js';
import pluginVue from 'eslint-plugin-vue';
import tseslint from 'typescript-eslint';
import prettier from 'eslint-config-prettier';

export default [
  eslint.configs.recommended,
  ...tseslint.configs.recommended,
  ...pluginVue.configs['flat/recommended'],
  prettier,
  {
    ignores: ['dist/', 'node_modules/'],
  },
];
```

`.prettierrc`:

```json
{
  "singleQuote": true,
  "trailingComma": "all",
  "printWidth": 100,
  "tabWidth": 2,
  "semi": true,
  "vueIndentScriptAndStyle": false
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
    "*.{ts,vue}": ["eslint --fix", "prettier --write"],
    "*.{json,md,css}": ["prettier --write"]
  }
}
```

### Vitest (Testing)

```bash
npm install -D vitest @testing-library/vue @testing-library/jest-dom jsdom
```

En `vite.config.ts`:

```typescript
/// <reference types="vitest" />
import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import path from 'path';

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: { '@': path.resolve(__dirname, './src') },
  },
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: './src/test/setup.ts',
  },
});
```

Crea `src/test/setup.ts`:

```typescript
import '@testing-library/jest-dom';
```

Ejemplo de test:

```typescript
// src/features/home/HomePage.test.ts
import { render, screen } from '@testing-library/vue';
import { describe, it, expect } from 'vitest';
import { createTestingPinia } from '@pinia/testing';
import HomePage from './HomePage.vue';

describe('HomePage', () => {
  it('renders heading', () => {
    render(HomePage, {
      global: {
        plugins: [createTestingPinia()],
      },
    });
    expect(screen.getByText('Bienvenido')).toBeInTheDocument();
  });
});
```

> Instala `@pinia/testing` para mockear stores en tests: `npm install -D @pinia/testing`

---

## 📜 Scripts Útiles

```json
{
  "scripts": {
    "dev": "vite",
    "build": "vue-tsc -b && vite build",
    "preview": "vite preview",
    "test": "vitest",
    "test:run": "vitest run",
    "test:coverage": "vitest run --coverage",
    "lint": "eslint .",
    "lint:fix": "eslint . --fix",
    "format": "prettier --write \"src/**/*.{ts,vue,css,json}\"",
    "type-check": "vue-tsc --noEmit"
  }
}
```

---

## ✅ Checklist de Setup

- [ ] Proyecto creado con Vite + Vue 3 + TypeScript
- [ ] Estructura de carpetas feature-based creada
- [ ] Path aliases (`@/`) configurados
- [ ] Vue Router con lazy loading y navigation guards
- [ ] Pinia store con persistencia
- [ ] TanStack Query con cliente Axios
- [ ] Variables de entorno (`.env`) configuradas
- [ ] Layout con TheHeader + TheFooter
- [ ] Componentes de página (Home, About, 404)
- [ ] Composables de autenticación
- [ ] ESLint + Prettier configurados
- [ ] Husky + lint-staged para pre-commit
- [ ] Vitest + Testing Library configurados
- [ ] Tests básicos pasando

---

> **Hane Boilerplates** — Vue.js Setup Guide
