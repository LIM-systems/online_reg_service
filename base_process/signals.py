# base_process/signals.py

from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.conf import settings
from base_process.models.about_company import AboutCompany
import os


@receiver(post_migrate)
def create_about_company(sender, **kwargs):
    """
    Создаёт запись AboutCompany с дефолтными изображениями, если её ещё нет.
    """
    if sender.name == 'base_process':
        # Определяем относительные пути к изображениям
        logo_path = 'about_company/default_logo.png'
        image_path = 'about_company/default_image.jpg'

        # Полные пути к изображениям
        full_logo_path = os.path.join(settings.MEDIA_ROOT, logo_path)
        full_image_path = os.path.join(settings.MEDIA_ROOT, image_path)

        # Проверяем, существуют ли файлы
        logo_exists = os.path.isfile(full_logo_path)
        image_exists = os.path.isfile(full_image_path)

        if not logo_exists:
            print(
                f"Предупреждение: Логотип не найден по пути {full_logo_path}")
        if not image_exists:
            print(f"Предупреждение: Фото не найдено по пути {full_image_path}")

        # Создаём запись с указанными путями к изображениям
        AboutCompany.objects.get_or_create(
            pk=1,
            defaults={
                'name': 'Название компании',
                'description': '',
                'logo': logo_path if logo_exists else '',
                'image': image_path if image_exists else '',
                'greeting': 'Добро пожаловать!',
                'address': '',
                'work_days': '5/2',
                'work_time': '09:00-18:00',
                'phone': '+79000000000',
            }
        )
