from django.db import models
from django.core.exceptions import ValidationError


# Программа лояльности

class LoyaltyProgram(models.Model):
    auto_toggle = models.BooleanField(verbose_name='Автоматический режим', default=True,
                                      help_text="Автоматически подключать программу лояльности клиентам при наличии акций, абонементов и сертификатов")
    toggle = models.BooleanField(verbose_name='Включена', default=False,
                                 help_text='Включить/выключить программу лояльности для отображения у клиентов')

    class Meta:
        verbose_name = 'Программа лояльности (вкл/выкл)'
        verbose_name_plural = 'Программа лояльности (вкл/выкл)'

    def __str__(self):
        return 'Программа лояльности'


class PromotionBase(models.Model):
    '''Базовая модель всех акций'''
    name = models.CharField(max_length=255, verbose_name='Название акции')
    description = models.TextField(verbose_name='Описание', blank=True)
    image = models.ImageField(upload_to='promotions/', verbose_name='Картинка акции',
                              null=True, blank=True)
    is_active = models.BooleanField(verbose_name='Активна', default=True)

    class Meta:
        abstract = True


class PromotionHasDates(models.Model):
    '''С датами'''
    discount = models.IntegerField(
        verbose_name='Скидка (%)', help_text='Введите процент скидки')
    date_start = models.DateTimeField(
        verbose_name='Дата начала', null=True, blank=True)
    date_end = models.DateTimeField(
        verbose_name='Дата окончания', null=True, blank=True)

    class Meta:
        abstract = True


class PromotionHasPeriod(models.Model):
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


class AbonementsJournal(models.Model):
    '''Журнал покупок абонементов'''
    client_name = models.ForeignKey(
        'base_process.Client', verbose_name='Клиент', on_delete=models.CASCADE)
    purchased_abonement = models.ForeignKey(
        Abonement, verbose_name='Абонемент', on_delete=models.CASCADE)
    date_time = models.DateTimeField(
        verbose_name='Дата покупки', auto_now_add=True)

    class Meta:
        verbose_name = 'Журнал покупок абонементов'
        verbose_name_plural = 'Журнал покупок абонементов'

    def __str__(self):
        return f'{self.client_name} - {self.purchased_abonement}'


class CertificatesJournal(models.Model):
    '''Журнал покупок сертификатов'''
    client_name = models.ForeignKey(
        'base_process.Client', verbose_name='Клиент', on_delete=models.CASCADE)
    purchased_certificate = models.ForeignKey(
        Certificate, verbose_name='Сертификат', on_delete=models.CASCADE)
    date_time = models.DateTimeField(
        verbose_name='Дата покупки', auto_now_add=True)

    class Meta:
        verbose_name = 'Журнал покупок сертификатов'
        verbose_name_plural = 'Журнал покупок сертификатов'

    def __str__(self):
        return f'{self.client_name} - {self.purchased_certificate}'


# Чат с админом

class ChatWithAdmin(models.Model):
    is_active = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Чат с админом (вкл/выкл)'
        verbose_name_plural = 'Чат с админом (вкл/выкл)'

    def __str__(self):
        return 'Чат с админом'

    def save(self, *args, **kwargs):
        if not self.pk and ChatWithAdmin.objects.exists():
            raise ValidationError(
                'Только одна запись ChatWithAdmin может существовать.')
        super().save(*args, **kwargs)
