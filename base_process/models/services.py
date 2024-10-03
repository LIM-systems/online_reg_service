from django.db import models
from PIL import Image


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
    image = models.ImageField(upload_to='services/', verbose_name='Картинка услуги',
                              null=True, blank=True)
    price = models.IntegerField(verbose_name='Цена(рублей)')

    def save(self, *args, **kwargs):
        '''Редактирование размеров картинки при необходимости'''
        super().save(*args, **kwargs)

        if self.image:
            max_width = 512
            max_height = 512
            img = Image.open(self.image.path)

            # Проверка размеров и изменение, если необходимо
            if img.width > max_width or img.height > max_height:
                new_size = (min(img.width, max_width),
                            min(img.height, max_height))
                img.thumbnail(new_size)
                img.save(self.image.path)

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'

    def __str__(self):
        return self.name
