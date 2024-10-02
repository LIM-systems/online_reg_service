from django.db import models
from base_process.models.users import *


# Программа лояльности

class PromotionBase(models.Model):
    '''Базовая модель всех акций'''
    name = models.CharField(max_length=255, verbose_name='Название акции')
    description = models.TextField(verbose_name='Описание', blank=True)
    image = models.ImageField(upload_to='promotions/', verbose_name='Картинка акции',
                              null=True, blank=True)
    is_active = models.BooleanField(verbose_name='Активна', default=True)

    class Meta:
        abstract = True


class PromotionHasDates(PromotionBase):
    '''С датами'''
    date_start = models.DateTimeField(
        verbose_name='Дата начала', null=True, blank=True)
    date_end = models.DateTimeField(
        verbose_name='Дата окончания', null=True, blank=True)

    class Meta:
        abstract = True


class PromotionHasPeriod(PromotionBase):
    '''С периодом'''
    period = models.IntegerField(
        verbose_name='Период (дни)', help_text='Введите количество дней', null=True, blank=True)

    class Meta:
        abstract = True


class Promotion(PromotionBase, PromotionHasDates):
    '''Акции'''

    class Meta:
        verbose_name = 'Акция'
        verbose_name_plural = 'Акции'

    def __str__(self):
        return self.name


class Certificate(PromotionBase, PromotionHasPeriod):
    '''Сертификаты'''

    class Meta:
        verbose_name = 'Сертификат'
        verbose_name_plural = 'Сертификаты'

    def __str__(self):
        return self.name


class Abonement(PromotionBase, PromotionHasPeriod):
    '''Абонементы'''

    class Meta:
        verbose_name = 'Абонемент'
        verbose_name_plural = 'Абонементы'

    def __str__(self):
        return self.name


class PromotionJournal(models.Model):
    '''Журнал покупок абонементов'''
    client = models.ForeignKey(
        Client, verbose_name='Клиент', on_delete=models.CASCADE)
    purchased_abonement = models.ForeignKey(
        Abonement, verbose_name='Акция', on_delete=models.CASCADE)
    date_time = models.DateTimeField(
        verbose_name='Дата покупки', auto_now_add=True)

    class Meta:
        verbose_name = 'Журнал покупок абонементов'
        verbose_name_plural = 'Журнал покупок абонементов'

    def __str__(self):
        return f'{self.client} - {self.purchased_abonement}'


# Чат с админом

class ChatWithAdmin(models.Model):
    is_active = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Чат с админом'
        verbose_name_plural = 'Чат с админом'

    def __str__(self):
        return f'Чат с админом'
