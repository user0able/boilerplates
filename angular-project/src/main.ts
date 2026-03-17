import * as Sentry from "@sentry/angular";
import { bootstrapApplication } from '@angular/platform-browser';
import { appConfig } from './app/app.config';
import { App } from './app/app';

Sentry.init({
    dsn: "https://a000000000@o0000000000000000000.ingest.us.sentry.io/0000000000000000",
    integrations: [Sentry.browserTracingIntegration()],
    tracesSampleRate: 1,
    enableLogs: true,
    sendDefaultPii: true
});

bootstrapApplication(App, appConfig)
    .catch((err) => console.error(err));