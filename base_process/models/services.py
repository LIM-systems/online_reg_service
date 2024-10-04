from django.db import models
from PIL import Image

from utils.models import validate_image_or_svg


class Categories(models.Model):
    '''Категории услуг'''
    name = models.CharField(max_length=255, verbose_name='Название')
    pic = models.ImageField(upload_to='categories/',
                            verbose_name='Картинка', null=True, blank=True)

    class Meta:
        verbose_name = 'Категорию'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Service(models.Model):
    '''Услуги'''
    name = models.CharField(max_length=255, verbose_name='Название услуги')
    services_categories = models.ManyToManyField(
        Categories, verbose_name='Категории', blank=True)
    duration = models.IntegerField(
        verbose_name='Длительность выполнения (минут)')
    description = models.TextField(verbose_name='Описание', blank=True)
    image = models.FileField(upload_to='services/', verbose_name='Картинка услуги',
                             null=True, blank=True, validators=[validate_image_or_svg])
    price = models.IntegerField(verbose_name='Цена(рублей)')

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'

    def __str__(self):
        return self.name
