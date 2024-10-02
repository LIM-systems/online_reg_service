from django.db import models
from utils.models import email_regex, phone_regex


class Person(models.Model):
    title = models.CharField(max_length=12)
    name = models.CharField(max_length=12)

    class Meta:
        verbose_name = 'Персона'
        verbose_name_plural = 'Персона'

    def __str__(self):
        return self.name


class Client(models.Model):
    '''Клиенты'''
    name = models.CharField(
        max_length=255, verbose_name='Имя',
        help_text='Введите имя клиента')
    email = models.CharField(
        validators=[email_regex],
        max_length=254, verbose_name='Email', help_text='укажите email')
    phone = models.CharField(
        validators=[phone_regex],
        max_length=12, verbose_name='Телефон',
        default='+7', help_text='Введите телефон в формате +79001112233')
    tg_id = models.BigIntegerField(
        verbose_name='Телеграм ID', null=True, blank=True)
    last_visit_bot = models.DateTimeField(
        verbose_name='Последнее посещение бота', blank=True, null=True)
    last_visit_web = models.DateTimeField(
        verbose_name='Последнее посещение web', blank=True, null=True)
    comment = models.TextField(
        verbose_name='Комментарий', null=True, blank=True)
    is_blocked = models.BooleanField(
        verbose_name='Бот заблокирован', null=True, blank=True)

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return f'{self.name} - {self.phone}'


class Master(models.Model):
    '''Мастера'''
    name = models.ForeignKey(
        to=Client, on_delete=models.CASCADE, verbose_name='Имя')
    description = models.TextField(verbose_name='Описание')
    services = models.ManyToManyField(
        'Service', verbose_name='Услуги', blank=True)
    rate = models.FloatField(
        default=0, verbose_name='Оценка', null=True, blank=True)
    photo = models.ImageField(
        upload_to='masters/',
        verbose_name='Фото мастера',)

    class Meta:
        verbose_name = 'Мастер'
        verbose_name_plural = 'Мастера'

    def __str__(self):
        return self.name.name
