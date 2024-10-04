from django.db import models
from add_funcs.models import Promotion
from base_process.models.users import *
from base_process.models.services import *
from utils.models import END_WORK_TIME_DEFAULT, START_WORK_TIME_DEFAULT


class MasterSchedule(models.Model):
    '''Расписание мастера'''
    master = models.ForeignKey(
        Master, on_delete=models.CASCADE, verbose_name='Мастер')
    date = models.DateField(verbose_name='Рабочий день')
    start_time = models.TimeField(
        verbose_name='Начало работы', default=START_WORK_TIME_DEFAULT)
    end_time = models.TimeField(
        verbose_name='Конец работы', default=END_WORK_TIME_DEFAULT)

    class Meta:
        verbose_name = 'График работы мастера'
        verbose_name_plural = 'Графики работы мастеров'

    def __str__(self):
        return f'{self.master} - {self.date}'


class VisitJournal(models.Model):
    '''Журнал записи клиентов'''
    MATH_ACTIONS = (('plus', 'Прибавление'), ('minus', 'Вычитание'))

    visit_client = models.ForeignKey(
        Client, on_delete=models.CASCADE, verbose_name='Клиент',)
    visit_master = models.ForeignKey(
        Master, on_delete=models.CASCADE, verbose_name='Мастер')
    create_date = models.DateTimeField(
        verbose_name='Дата создания записи', auto_now_add=True)
    visit_date = models.DateTimeField(verbose_name='Дата посещения')
    visit_service = models.ForeignKey(
        Service, on_delete=models.CASCADE, verbose_name='Услуга')
    confirmation = models.DateTimeField(
        verbose_name='Подтверждение', blank=True, null=True)
    cancel = models.BooleanField(default=False, verbose_name='Услуга отменена')
    finish = models.BooleanField(default=False, verbose_name='Услуга оказана')
    rate = models.IntegerField(
        verbose_name='Оценка', null=True, blank=True)
    comment = models.TextField(
        verbose_name='Комментарий', blank=True, null=True)
    note = models.TextField(
        verbose_name='Заметка', blank=True, null=True)
    promotion_discount = models.ManyToManyField(
        Promotion, verbose_name='Акция', blank=True)
    math_action = models.CharField(
        max_length=255, verbose_name='Действие',
        choices=MATH_ACTIONS, default='plus')
    math_value = models.IntegerField(
        verbose_name='Значение', null=True, blank=True,
        help_text='Значение должно быть кратным 15')

    class Meta:
        verbose_name = 'Журнал посещений'
        verbose_name_plural = 'Журнал посещений'

    def __str__(self):
        return f'{self.visit_client} - {self.visit_date}'
