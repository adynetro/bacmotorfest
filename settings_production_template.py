# Production Settings Override
# Copy this file to motorfest/settings_local.py and customize for production

import os
from motorfest.settings import *

# Security Settings
DEBUG = False
SECRET_KEY = "CHANGE-ME-TO-A-SECURE-KEY"  # Generate with: python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
ALLOWED_HOSTS = ["your-domain.com", "www.your-domain.com"]

# HTTPS/Security
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Static files
STATIC_ROOT = "/var/www/bacmotorfest/static"
STATIC_URL = "/static/"

# Media files
MEDIA_ROOT = "/var/www/bacmotorfest/media"
MEDIA_URL = "/media/"

# Database - SQLite
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "/var/www/bacmotorfest/db.sqlite3",
    }
}

# Email Configuration (optional - for notifications)
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.example.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = 'your-email@example.com'
# EMAIL_HOST_PASSWORD = 'your-password'
# DEFAULT_FROM_EMAIL = 'noreply@bacmotorfest.com'

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/bacmotorfest/django.log',
            'maxBytes': 1024 * 1024 * 10,  # 10MB
            'backupCount': 10,
        },
    },
    'root': {
        'handlers': ['file'],
        'level': 'ERROR',
    },
}
