# 📦 Hane Boilerplates

> Colección de boilerplates listos para usar con buenas prácticas, estructura modular y herramientas esenciales para comenzar proyectos rápidamente.

---

## 🎯 ¿Qué es esto?

**Hane Boilerplates** es un repositorio con guías paso a paso y configuraciones base para crear proyectos con los frameworks más populares. Cada boilerplate incluye:

- Estructura de carpetas probada y escalable
- Configuraciones de desarrollo y producción
- Integración de herramientas de calidad de código
- Patrones y buenas prácticas aplicadas
- Checklists para validar el setup

---

## 📚 Boilerplates Disponibles

| Stack | Archivo | Estado | Descripción |
|-------|---------|--------|-------------|
| 🅰️ Angular | [Angular.md](Angular.md) | ✅ Completo | Frontend con Angular Material, lazy loading, interceptors |
| 🐍 Django | [Django.md](Django.md) | ✅ Completo | Backend API REST con DRF, JWT, Swagger |
| ⚛️ React | — | 🔜 Próximo | Frontend con Vite, React Router, Zustand |
| 🟢 Node.js / Express | — | 🔜 Próximo | Backend API REST con Express, Prisma |
| 🐳 Docker | — | 📋 Planeado | Docker Compose para Angular + Django |
| 🔗 Fullstack | — | 📋 Planeado | Angular + Django integrados con Docker |

---

## 🗺️ Roadmap

### Fase 1 — Fundamentos ✅

- [x] Boilerplate Angular (estructura, routing, servicios, interceptors)
- [x] Boilerplate Django (DRF, JWT, settings por entorno, Swagger)
- [x] README principal con roadmap

### Fase 2 — Más Frameworks

- [ ] **React.md** — Boilerplate con Vite + React + TypeScript
  - React Router v7, Zustand, TanStack Query
  - Estructura feature-based similar a Angular
- [ ] **Node.md** — Backend con Express + TypeScript
  - Prisma ORM, validación con Zod
  - Estructura por capas (controllers, services, repositories)
- [ ] **Next.md** — Fullstack con Next.js + App Router
  - Server Components, Server Actions
  - Auth con NextAuth.js

### Fase 3 — DevOps & Infraestructura

- [ ] **Docker.md** — Docker Compose para cada stack
  - Dockerfile optimizados con multi-stage builds
  - Compose para desarrollo local (hot reload)
  - Compose para producción
- [ ] **CI-CD.md** — Pipelines de CI/CD
  - GitHub Actions para lint, test, build, deploy
  - Configuraciones para Angular, Django, React, Node

### Fase 4 — Integraciones

- [ ] **Fullstack.md** — Angular + Django integrados
  - Comunicación frontend-backend
  - Autenticación compartida (JWT)
  - Docker Compose unificado
- [ ] **Testing.md** — Estrategias de testing por stack
  - Unit, integration, e2e
  - Jest, Pytest, Cypress/Playwright

### Fase 5 — Avanzado

- [ ] **Monorepo.md** — Configuración con Nx o Turborepo
- [ ] **Deploy.md** — Guías de despliegue (Railway, Vercel, AWS, DigitalOcean)
- [ ] **Auth.md** — Patrones de autenticación avanzados (OAuth, SAML, SSO)

---

## ✅ TODO List

### Prioridad Alta 🔴

- [ ] Probar boilerplate Angular de punta a punta
- [ ] Probar boilerplate Django de punta a punta
- [ ] Agregar sección de troubleshooting a cada guía
- [ ] Crear script de scaffolding automático por boilerplate

### Prioridad Media 🟡

- [ ] Boilerplate React (Vite + TypeScript)
- [ ] Boilerplate Node.js (Express + TypeScript)
- [ ] Docker Compose para Angular + Django
- [ ] GitHub Actions básico (lint + test)

### Prioridad Baja 🟢

- [ ] Boilerplate Next.js
- [ ] Guía de monorepo
- [ ] Guías de deploy por plataforma
- [ ] Templates de `.env` por stack
- [ ] CLI propia para generar boilerplates (`npx hane-create`)

### Ideas Futuras 💡

- [ ] Boilerplate Flutter / React Native (mobile)
- [ ] Boilerplate FastAPI como alternativa a Django
- [ ] Boilerplate NestJS como alternativa a Express
- [ ] Integración con Terraform / Pulumi (IaC)
- [ ] Templates de Figma que matcheen con los boilerplates

---

## 🚀 Cómo Usar

1. **Elige un boilerplate** de la tabla de arriba
2. **Abre el archivo `.md`** correspondiente
3. **Sigue los pasos** en orden — cada guía está diseñada para ejecutarse secuencialmente
4. **Usa el checklist** al final de cada guía para verificar que todo está configurado

---

## 📁 Estructura del Repositorio

```
boilerplates/
├── README.md          # ← Estás aquí
├── Angular.md         # Guía completa de Angular
├── Django.md          # Guía completa de Django
└── ...                # Futuras guías
```

---

## 🤝 Contribuir

Si quieres agregar un boilerplate o mejorar uno existente:

1. Sigue la estructura y formato de los boilerplates existentes
2. Incluye tabla de contenidos, requisitos, estructura de carpetas y checklist
3. Asegúrate de que los pasos sean reproducibles y funcionen de punta a punta

---

> **Hane Boilerplates** — Empieza rápido, construye bien. 🏗️
