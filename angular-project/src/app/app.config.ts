import * as Sentry from "@sentry/angular";
import {
  ApplicationConfig,
  provideBrowserGlobalErrorListeners,
  ErrorHandler,
  provideAppInitializer,
  inject,
} from '@angular/core';
import { provideRouter, Router } from '@angular/router';

import { routes } from './app.routes';
import { provideClientHydration, withEventReplay } from '@angular/platform-browser';

export const appConfig: ApplicationConfig = {
  providers: [
    provideBrowserGlobalErrorListeners(),
    provideRouter(routes),
    provideClientHydration(withEventReplay()),
    {
      provide: ErrorHandler,
      useValue: Sentry.createErrorHandler()
    },
    {
      provide: Sentry.TraceService,
      deps: [Router]
    },
    provideAppInitializer(() => {
      inject(Sentry.TraceService);
    })
  ]
};