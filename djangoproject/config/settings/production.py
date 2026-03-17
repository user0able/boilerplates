from .base import *  # noqa: F401, F403
import sentry_sdk

DEBUG = False
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")
DATABASES = {
    "default": env.db("DATABASE_URL"),
}
CORS_ALLOWED_ORIGINS = env.list("CORS_ALLOWED_ORIGINS", default=[])
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = env.bool("SECURE_SSL_REDIRECT", default=True)
sentry_sdk.init(
    dsn=env("SENTRY_DSN", default=""),
    traces_sample_rate=0.1,
)