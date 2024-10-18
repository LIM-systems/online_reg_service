from django.conf.locale import de
from django.db import models
from utils.models import phone_regex


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
    email = models.EmailField(
        max_length=254, verbose_name='Email',
        help_text='укажите email')
    phone = models.CharField(
        validators=[phone_regex],
        max_length=12, verbose_name='Телефон',
        default='+7', help_text='Введите телефон в формате +79001112233')
    tg_id = models.BigIntegerField(
        verbose_name='Телеграм ID', null=True, blank=True)
    comment = models.TextField(
        verbose_name='Комментарий', null=True, blank=True)

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return f'{self.name} - {self.phone}'


class ClientActivity(models.Model):
    '''Активность клиентов'''
    name = models.ForeignKey(
        to=Client, on_delete=models.CASCADE, verbose_name='Имя')
    last_visit_bot = models.DateTimeField(
        verbose_name='Последнее посещение бота', blank=True, null=True)
    last_visit_web = models.DateTimeField(
        verbose_name='Последнее посещение web', blank=True, null=True)
    is_blocked = models.BooleanField(
        verbose_name='Бот заблокирован', null=True, blank=True)

    class Meta:
        verbose_name = 'Активность клиента'
        verbose_name_plural = 'Активность клиентов'

    def __str__(self):
        return f'{self.name.name}'


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
        verbose_name='Фото мастера', default='masters/default.png')
    is_active_role = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Мастер'
        verbose_name_plural = 'Мастера'

    def __str__(self):
        return self.name.name


class Admin(models.Model):
    '''Администраторы'''
    name = models.ForeignKey(
        Client, on_delete=models.CASCADE, verbose_name='Назначить администратора')
    is_active_role = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Администратор'
        verbose_name_plural = 'Администраторы'

    def __str__(self):
        return self.name.name
