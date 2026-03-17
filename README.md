npm install -g @angular/cli

ng new <project-name>
cd <project-name>

- add Angular Material:
ng add @angular/material

- add animations:
npm install @angular/animations

- add environment variables:
ng generate environment

- add:
src/app/core
src/app/core/models
src/app/core/services
src/app/features
src/app/features/about
src/app/features/home
src/app/features/not-found
src/app/shared
src/app/shared/directives
src/app/shared/pipes
src/app/shared/ui
src/app/shared/ui/footer
src/app/shared/ui/header
src/assets/data/data-mock.json

- este tipo de estructura es solo una sugerencia, puedes adaptarla a tus necesidades y preferencias. Pero es importante mantener una organización clara y coherente para facilitar el desarrollo y mantenimiento de la aplicación. El nombre de este tipo de estructura es "feature-based structure" o "modular structure", ya que se organiza en torno a las características o módulos de la aplicación.
- para crear las carpetas con un comando, puedes usar el siguiente utilizando ng g:
ng g c features/about
ng g c features/home
ng g c features/not-found
ng g c shared/ui/footer
ng g c shared/ui/header
ng g class core/models --type=model
ng g service core/services // para APIs y otro para lógica de negocio
ng g interceptor core/services/interceptor
ng g guard core/services/guard
ng g pipe shared/pipes
ng g directive shared/directives
ng g environment environments/environment

- modifica el src/app.html para incluir el header y footer:
<app-header/>
<router-outlet/>
<app-footer/>

- install Sentry:
npx @sentry/wizard@latest -i angular
