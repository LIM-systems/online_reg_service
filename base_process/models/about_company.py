from django.db import models
from django.core.validators import RegexValidator
from utils.models import phone_regex


class AboutCompany(models.Model):
    '''О компании'''
    name = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(
        verbose_name='Описание', blank=True, null=True)
    logo = models.ImageField(upload_to='about_company/', verbose_name='Логотип',
                             null=True, blank=True)
    image = models.ImageField(upload_to='about_company/', verbose_name='Фото',
                              null=True, blank=True)
    greeting = models.TextField(verbose_name='Приветствие для клиентов')
    address = models.CharField(max_length=255, verbose_name='Адрес')
    work_days = models.CharField(
        max_length=255, verbose_name='Рабочие дни', help_text='5/2, 2/2, 3/3 и пр.')
    work_time = models.CharField(max_length=255, verbose_name='Рабочие часы')
    phone = models.CharField(
        validators=[phone_regex],
        max_length=12, verbose_name='Телефон',
        default='+7', help_text='Введите телефон в формате +79001112233')
