from .base import *

ALLOWED_HOSTS = ['server.com', 'www.server.com']

# Настройки безопасности
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Логирование
LOGGING = {
    # Ваши настройки логирования
}

# Статические и медиа-файлы
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
