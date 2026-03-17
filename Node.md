# 🟢 Node.js / Express Boilerplate

> Guía paso a paso para crear una API REST con Express, TypeScript, Prisma ORM y herramientas esenciales de producción.

---

## 📋 Tabla de Contenidos

- [Requisitos Previos](#-requisitos-previos)
- [Creación del Proyecto](#-creación-del-proyecto)
- [Dependencias Esenciales](#-dependencias-esenciales)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Configuración de TypeScript](#-configuración-de-typescript)
- [Servidor Express](#-servidor-express)
- [Routing y Controllers](#-routing-y-controllers)
- [Prisma ORM](#-prisma-orm)
- [Validación con Zod](#-validación-con-zod)
- [Autenticación JWT](#-autenticación-jwt)
- [Manejo de Errores](#-manejo-de-errores)
- [Variables de Entorno](#-variables-de-entorno)
- [Herramientas de Calidad](#-herramientas-de-calidad)
- [Scripts Útiles](#-scripts-útiles)

---

## 🔧 Requisitos Previos

| Herramienta | Versión Mínima | Instalación                                                  |
| ----------- | -------------- | ------------------------------------------------------------ |
| Node.js     | 18.x           | [nodejs.org](https://nodejs.org)                             |
| npm         | 9.x            | Incluido con Node.js                                         |
| PostgreSQL  | 15.x           | [postgresql.org](https://postgresql.org) (o SQLite para dev) |

Verificar instalación:

```bash
node -v
npm -v
```

---

## 🚀 Creación del Proyecto

```bash
mkdir <nombre-del-proyecto> && cd <nombre-del-proyecto>
npm init -y
```

---

## 📦 Dependencias Esenciales

### Runtime

```bash
npm install express cors helmet morgan compression cookie-parser \
  @prisma/client zod jsonwebtoken bcryptjs dotenv http-status-codes
```

### Desarrollo

```bash
npm install -D typescript tsx @types/node @types/express @types/cors \
  @types/morgan @types/cookie-parser @types/jsonwebtoken @types/bcryptjs \
  prisma vitest @faker-js/faker supertest @types/supertest \
  eslint prettier eslint-config-prettier
```

---

## 🏗️ Estructura del Proyecto

Estructura por **capas** (layers), separando responsabilidades de forma clara.

```
src/
├── config/                            # Configuración centralizada
│   ├── env.ts                         # Variables de entorno tipadas
│   ├── database.ts                    # Conexión a BD (Prisma client)
│   └── cors.ts                       # Configuración de CORS
│
├── modules/                           # Módulos por dominio
│   ├── users/
│   │   ├── user.controller.ts         # Handlers de requests
│   │   ├── user.service.ts            # Lógica de negocio
│   │   ├── user.repository.ts         # Acceso a datos (Prisma)
│   │   ├── user.routes.ts             # Definición de rutas
│   │   ├── user.schema.ts             # Validación con Zod
│   │   └── user.test.ts              # Tests del módulo
│   │
│   └── auth/
│       ├── auth.controller.ts
│       ├── auth.service.ts
│       ├── auth.routes.ts
│       ├── auth.schema.ts
│       └── auth.test.ts
│
├── shared/                            # Código compartido entre módulos
│   ├── middleware/
│   │   ├── auth.middleware.ts         # Verificación de JWT
│   │   ├── validate.middleware.ts     # Validación de schemas
│   │   └── error.middleware.ts        # Manejo global de errores
│   ├── errors/
│   │   └── app-error.ts              # Clase de error personalizada
│   └── utils/
│       ├── logger.ts                  # Logger
│       └── async-handler.ts           # Wrapper para async controllers
│
├── app.ts                             # Configuración de Express
├── server.ts                          # Entry point (arranque del server)
└── routes.ts                          # Router principal
│
prisma/
├── schema.prisma                      # Schema de Prisma
├── migrations/                        # Migraciones auto-generadas
└── seed.ts                            # Seed de datos iniciales
│
.env                                   # Variables de entorno
.env.example
tsconfig.json
package.json
```

### Crear la estructura de carpetas

```bash
mkdir -p src/{config,modules/{users,auth},shared/{middleware,errors,utils}} prisma
```

---

## ⚙️ Configuración de TypeScript

### `tsconfig.json`

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "lib": ["ES2022"],
    "outDir": "dist",
    "rootDir": "src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,
    "baseUrl": ".",
    "paths": {
      "@config/*": ["src/config/*"],
      "@modules/*": ["src/modules/*"],
      "@shared/*": ["src/shared/*"]
    }
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

> **Nota:** Se usa `tsx` en desarrollo para ejecutar TypeScript directamente sin compilar.

---

## 🖥️ Servidor Express

### `src/app.ts`

```typescript
import express from 'express';
import cors from 'cors';
import helmet from 'helmet';
import morgan from 'morgan';
import compression from 'compression';
import cookieParser from 'cookie-parser';
import { corsConfig } from './config/cors.js';
import { router } from './routes.js';
import { errorMiddleware } from './shared/middleware/error.middleware.js';

const app = express();

// Security
app.use(helmet());
app.use(cors(corsConfig));

// Parsing
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true }));
app.use(cookieParser());

// Logging & Compression
app.use(morgan('dev'));
app.use(compression());

// Health check
app.get('/health', (_req, res) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

// API Routes
app.use('/api/v1', router);

// Global error handler (must be last)
app.use(errorMiddleware);

export { app };
```

### `src/server.ts`

```typescript
import { app } from './app.js';
import { env } from './config/env.js';
import { prisma } from './config/database.js';

async function main() {
  // Verify database connection
  await prisma.$connect();
  console.log('✅ Database connected');

  app.listen(env.PORT, () => {
    console.log(`🚀 Server running on http://localhost:${env.PORT}`);
    console.log(`📚 Environment: ${env.NODE_ENV}`);
  });
}

main().catch((err) => {
  console.error('❌ Failed to start server:', err);
  process.exit(1);
});

// Graceful shutdown
process.on('SIGTERM', async () => {
  console.log('🛑 SIGTERM received. Shutting down...');
  await prisma.$disconnect();
  process.exit(0);
});
```

### `src/config/env.ts`

```typescript
import dotenv from 'dotenv';
import { z } from 'zod';

dotenv.config();

const envSchema = z.object({
  NODE_ENV: z.enum(['development', 'production', 'test']).default('development'),
  PORT: z.coerce.number().default(3000),
  DATABASE_URL: z.string().url(),
  JWT_SECRET: z.string().min(32),
  JWT_EXPIRES_IN: z.string().default('30m'),
  CORS_ORIGIN: z.string().default('http://localhost:5173'),
});

export const env = envSchema.parse(process.env);
```

### `src/config/database.ts`

```typescript
import { PrismaClient } from '@prisma/client';
import { env } from './env.js';

export const prisma = new PrismaClient({
  log: env.NODE_ENV === 'development' ? ['query', 'warn', 'error'] : ['error'],
});
```

### `src/config/cors.ts`

```typescript
import type { CorsOptions } from 'cors';
import { env } from './env.js';

export const corsConfig: CorsOptions = {
  origin: env.CORS_ORIGIN.split(','),
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'PATCH', 'DELETE'],
  allowedHeaders: ['Content-Type', 'Authorization'],
};
```

---

## 🛤️ Routing y Controllers

### Router Principal (`src/routes.ts`)

```typescript
import { Router } from 'express';
import { userRoutes } from './modules/users/user.routes.js';
import { authRoutes } from './modules/auth/auth.routes.js';

export const router = Router();

router.use('/users', userRoutes);
router.use('/auth', authRoutes);
```

### User Module

#### `src/modules/users/user.routes.ts`

```typescript
import { Router } from 'express';
import { UserController } from './user.controller.js';
import { authMiddleware } from '../../shared/middleware/auth.middleware.js';
import { validate } from '../../shared/middleware/validate.middleware.js';
import { createUserSchema, updateUserSchema } from './user.schema.js';

export const userRoutes = Router();
const controller = new UserController();

userRoutes.get('/', authMiddleware, controller.findAll);
userRoutes.get('/:id', authMiddleware, controller.findById);
userRoutes.post('/', validate(createUserSchema), controller.create);
userRoutes.put('/:id', authMiddleware, validate(updateUserSchema), controller.update);
userRoutes.delete('/:id', authMiddleware, controller.delete);
```

#### `src/modules/users/user.controller.ts`

```typescript
import type { Request, Response } from 'express';
import { StatusCodes } from 'http-status-codes';
import { UserService } from './user.service.js';
import { asyncHandler } from '../../shared/utils/async-handler.js';

const userService = new UserService();

export class UserController {
  findAll = asyncHandler(async (_req: Request, res: Response) => {
    const users = await userService.findAll();
    res.json(users);
  });

  findById = asyncHandler(async (req: Request, res: Response) => {
    const user = await userService.findById(req.params.id);
    res.json(user);
  });

  create = asyncHandler(async (req: Request, res: Response) => {
    const user = await userService.create(req.body);
    res.status(StatusCodes.CREATED).json(user);
  });

  update = asyncHandler(async (req: Request, res: Response) => {
    const user = await userService.update(req.params.id, req.body);
    res.json(user);
  });

  delete = asyncHandler(async (req: Request, res: Response) => {
    await userService.delete(req.params.id);
    res.status(StatusCodes.NO_CONTENT).send();
  });
}
```

#### `src/modules/users/user.service.ts`

```typescript
import { UserRepository } from './user.repository.js';
import { AppError } from '../../shared/errors/app-error.js';
import { StatusCodes } from 'http-status-codes';
import bcryptjs from 'bcryptjs';

const userRepo = new UserRepository();

export class UserService {
  async findAll() {
    return userRepo.findAll();
  }

  async findById(id: string) {
    const user = await userRepo.findById(id);
    if (!user) {
      throw new AppError('User not found', StatusCodes.NOT_FOUND);
    }
    return user;
  }

  async create(data: { email: string; username: string; password: string }) {
    const hashedPassword = await bcryptjs.hash(data.password, 12);
    return userRepo.create({ ...data, password: hashedPassword });
  }

  async update(id: string, data: { email?: string; username?: string }) {
    await this.findById(id); // throws if not found
    return userRepo.update(id, data);
  }

  async delete(id: string) {
    await this.findById(id);
    return userRepo.delete(id);
  }
}
```

#### `src/modules/users/user.repository.ts`

```typescript
import { prisma } from '../../config/database.js';

export class UserRepository {
  async findAll() {
    return prisma.user.findMany({
      select: { id: true, email: true, username: true, createdAt: true },
    });
  }

  async findById(id: string) {
    return prisma.user.findUnique({
      where: { id },
      select: { id: true, email: true, username: true, createdAt: true },
    });
  }

  async findByEmail(email: string) {
    return prisma.user.findUnique({ where: { email } });
  }

  async create(data: { email: string; username: string; password: string }) {
    return prisma.user.create({
      data,
      select: { id: true, email: true, username: true, createdAt: true },
    });
  }

  async update(id: string, data: { email?: string; username?: string }) {
    return prisma.user.update({
      where: { id },
      data,
      select: { id: true, email: true, username: true, createdAt: true },
    });
  }

  async delete(id: string) {
    return prisma.user.delete({ where: { id } });
  }
}
```

---

## 🗄️ Prisma ORM

### Inicializar Prisma

```bash
npx prisma init
```

### `prisma/schema.prisma`

```prisma
generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"   // o "sqlite" para desarrollo
  url      = env("DATABASE_URL")
}

model User {
  id        String   @id @default(cuid())
  email     String   @unique
  username  String   @unique
  password  String
  createdAt DateTime @default(now()) @map("created_at")
  updatedAt DateTime @updatedAt @map("updated_at")

  @@map("users")
}
```

### Comandos de Prisma

```bash
# Crear migración
npx prisma migrate dev --name init

# Aplicar migraciones en producción
npx prisma migrate deploy

# Regenerar cliente
npx prisma generate

# Abrir Prisma Studio (GUI)
npx prisma studio

# Seed de datos
npx prisma db seed
```

### Seed (`prisma/seed.ts`)

```typescript
import { PrismaClient } from '@prisma/client';
import bcryptjs from 'bcryptjs';

const prisma = new PrismaClient();

async function main() {
  const hashedPassword = await bcryptjs.hash('password123', 12);

  await prisma.user.upsert({
    where: { email: 'admin@example.com' },
    update: {},
    create: {
      email: 'admin@example.com',
      username: 'admin',
      password: hashedPassword,
    },
  });

  console.log('✅ Seed completed');
}

main()
  .catch((e) => {
    console.error(e);
    process.exit(1);
  })
  .finally(() => prisma.$disconnect());
```

En `package.json`:

```json
{
  "prisma": {
    "seed": "tsx prisma/seed.ts"
  }
}
```

---

## ✅ Validación con Zod

### Schemas (`src/modules/users/user.schema.ts`)

```typescript
import { z } from 'zod';

export const createUserSchema = z.object({
  body: z.object({
    email: z.string().email('Email inválido'),
    username: z.string().min(3, 'Mínimo 3 caracteres').max(30),
    password: z.string().min(8, 'Mínimo 8 caracteres'),
  }),
});

export const updateUserSchema = z.object({
  body: z.object({
    email: z.string().email('Email inválido').optional(),
    username: z.string().min(3).max(30).optional(),
  }),
  params: z.object({
    id: z.string(),
  }),
});

export type CreateUserInput = z.infer<typeof createUserSchema>['body'];
export type UpdateUserInput = z.infer<typeof updateUserSchema>['body'];
```

### Middleware de Validación (`src/shared/middleware/validate.middleware.ts`)

```typescript
import type { Request, Response, NextFunction } from 'express';
import type { ZodSchema } from 'zod';
import { StatusCodes } from 'http-status-codes';

export function validate(schema: ZodSchema) {
  return (req: Request, res: Response, next: NextFunction) => {
    const result = schema.safeParse({
      body: req.body,
      query: req.query,
      params: req.params,
    });

    if (!result.success) {
      res.status(StatusCodes.BAD_REQUEST).json({
        status: 'error',
        errors: result.error.flatten().fieldErrors,
      });
      return;
    }

    next();
  };
}
```

---

## 🔐 Autenticación JWT

### Auth Module (`src/modules/auth/auth.routes.ts`)

```typescript
import { Router } from 'express';
import { AuthController } from './auth.controller.js';
import { validate } from '../../shared/middleware/validate.middleware.js';
import { loginSchema, registerSchema } from './auth.schema.js';

export const authRoutes = Router();
const controller = new AuthController();

authRoutes.post('/register', validate(registerSchema), controller.register);
authRoutes.post('/login', validate(loginSchema), controller.login);
```

### `src/modules/auth/auth.service.ts`

```typescript
import bcryptjs from 'bcryptjs';
import jwt from 'jsonwebtoken';
import { UserRepository } from '../users/user.repository.js';
import { AppError } from '../../shared/errors/app-error.js';
import { StatusCodes } from 'http-status-codes';
import { env } from '../../config/env.js';

const userRepo = new UserRepository();

export class AuthService {
  async register(data: { email: string; username: string; password: string }) {
    const existing = await userRepo.findByEmail(data.email);
    if (existing) {
      throw new AppError('Email already registered', StatusCodes.CONFLICT);
    }

    const hashedPassword = await bcryptjs.hash(data.password, 12);
    const user = await userRepo.create({ ...data, password: hashedPassword });
    const token = this.generateToken(user.id);

    return { user, token };
  }

  async login(email: string, password: string) {
    const user = await userRepo.findByEmail(email);
    if (!user) {
      throw new AppError('Invalid credentials', StatusCodes.UNAUTHORIZED);
    }

    const isValid = await bcryptjs.compare(password, user.password);
    if (!isValid) {
      throw new AppError('Invalid credentials', StatusCodes.UNAUTHORIZED);
    }

    const token = this.generateToken(user.id);
    return {
      user: { id: user.id, email: user.email, username: user.username },
      token,
    };
  }

  private generateToken(userId: string): string {
    return jwt.sign({ sub: userId }, env.JWT_SECRET, {
      expiresIn: env.JWT_EXPIRES_IN,
    });
  }
}
```

### Auth Middleware (`src/shared/middleware/auth.middleware.ts`)

```typescript
import type { Request, Response, NextFunction } from 'express';
import jwt from 'jsonwebtoken';
import { StatusCodes } from 'http-status-codes';
import { env } from '../../config/env.js';
import { AppError } from '../errors/app-error.js';

export function authMiddleware(req: Request, _res: Response, next: NextFunction) {
  const authHeader = req.headers.authorization;

  if (!authHeader?.startsWith('Bearer ')) {
    throw new AppError('No token provided', StatusCodes.UNAUTHORIZED);
  }

  const token = authHeader.split(' ')[1];

  try {
    const decoded = jwt.verify(token, env.JWT_SECRET) as { sub: string };
    (req as Request & { userId: string }).userId = decoded.sub;
    next();
  } catch {
    throw new AppError('Invalid or expired token', StatusCodes.UNAUTHORIZED);
  }
}
```

---

## 🚨 Manejo de Errores

### `src/shared/errors/app-error.ts`

```typescript
export class AppError extends Error {
  constructor(
    message: string,
    public statusCode: number,
    public isOperational = true,
  ) {
    super(message);
    Object.setPrototypeOf(this, AppError.prototype);
  }
}
```

### `src/shared/middleware/error.middleware.ts`

```typescript
import type { Request, Response, NextFunction } from 'express';
import { StatusCodes } from 'http-status-codes';
import { AppError } from '../errors/app-error.js';

export function errorMiddleware(
  err: Error,
  _req: Request,
  res: Response,
  _next: NextFunction,
) {
  if (err instanceof AppError) {
    res.status(err.statusCode).json({
      status: 'error',
      message: err.message,
    });
    return;
  }

  console.error('Unexpected error:', err);

  res.status(StatusCodes.INTERNAL_SERVER_ERROR).json({
    status: 'error',
    message: 'Internal server error',
  });
}
```

### `src/shared/utils/async-handler.ts`

```typescript
import type { Request, Response, NextFunction } from 'express';

type AsyncFn = (req: Request, res: Response, next: NextFunction) => Promise<void>;

export function asyncHandler(fn: AsyncFn) {
  return (req: Request, res: Response, next: NextFunction) => {
    fn(req, res, next).catch(next);
  };
}
```

---

## 🔒 Variables de Entorno

### `.env.example`

```env
# Server
NODE_ENV=development
PORT=3000

# Database
DATABASE_URL="postgresql://user:password@localhost:5432/mydb?schema=public"
# DATABASE_URL="file:./dev.db"   # SQLite alternativo

# Auth
JWT_SECRET=tu-secret-key-de-al-menos-32-caracteres-aqui
JWT_EXPIRES_IN=30m

# CORS
CORS_ORIGIN=http://localhost:5173,http://localhost:4200
```

### `.gitignore`

```gitignore
node_modules/
dist/
.env
*.db
*.db-journal
```

---

## 🛠️ Herramientas de Calidad

### ESLint + Prettier

```bash
npm install -D eslint @eslint/js typescript-eslint eslint-config-prettier prettier
```

`eslint.config.js`:

```javascript
import eslint from '@eslint/js';
import tseslint from 'typescript-eslint';
import prettier from 'eslint-config-prettier';

export default tseslint.config(
  eslint.configs.recommended,
  ...tseslint.configs.recommended,
  prettier,
  {
    ignores: ['dist/', 'node_modules/'],
  },
);
```

`.prettierrc`:

```json
{
  "singleQuote": true,
  "trailingComma": "all",
  "printWidth": 100,
  "tabWidth": 2,
  "semi": true
}
```

### Vitest (Testing)

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    globals: true,
    environment: 'node',
    coverage: {
      provider: 'v8',
      reporter: ['text', 'html'],
    },
  },
});
```

---

## 📜 Scripts Útiles

```json
{
  "scripts": {
    "dev": "tsx watch src/server.ts",
    "build": "tsc",
    "start": "node dist/server.js",
    "lint": "eslint .",
    "lint:fix": "eslint . --fix",
    "format": "prettier --write \"src/**/*.ts\"",
    "test": "vitest",
    "test:run": "vitest run",
    "test:coverage": "vitest run --coverage",
    "db:migrate": "prisma migrate dev",
    "db:push": "prisma db push",
    "db:seed": "prisma db seed",
    "db:studio": "prisma studio",
    "db:generate": "prisma generate"
  }
}
```

---

## ✅ Checklist de Setup

- [ ] Proyecto Node.js + TypeScript inicializado
- [ ] Express configurado con middleware de seguridad (helmet, cors)
- [ ] Estructura por capas (controllers, services, repositories)
- [ ] Prisma ORM conectado a la base de datos
- [ ] Migraciones creadas y aplicadas
- [ ] Validación con Zod en endpoints
- [ ] Autenticación JWT implementada
- [ ] Manejo global de errores (`AppError` + middleware)
- [ ] Variables de entorno tipadas y validadas
- [ ] Health check endpoint (`/health`)
- [ ] ESLint + Prettier configurados
- [ ] Tests básicos pasando
- [ ] Seed de datos iniciales
- [ ] `.gitignore` configurado

---

> **Hane Boilerplates** — Node.js / Express Setup Guide
