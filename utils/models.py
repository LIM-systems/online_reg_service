from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import os

phone_regex = RegexValidator(
    regex=r'^\+7\d{10}$',
    message='Номер должен быть в формате +79001112233')

START_WORK_TIME_DEFAULT = '10:00:00'
END_WORK_TIME_DEFAULT = '21:00:00'


def validate_image_or_svg(file):
    ext = os.path.splitext(file.name)[1]  # Получаем расширение файла
    valid_extensions = ['.jpg', '.jpeg', '.png', '.svg']
    if not ext.lower() in valid_extensions:
        raise ValidationError(
            _('Недопустимый формат файла. Допустимы только изображения с расширениями: .jpg, .jpeg, .png, .svg.'))
