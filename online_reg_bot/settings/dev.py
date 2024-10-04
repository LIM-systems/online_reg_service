from .base import *

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '45.8.99.97']

# Настройки базы данных для разработки (если требуется)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Настройки для отладки почты
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
