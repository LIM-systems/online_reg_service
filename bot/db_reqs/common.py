from datetime import datetime
from django.db.models import Q
from asgiref.sync import sync_to_async

from base_process import models as base_mdls
from add_funcs import models as add_models


@sync_to_async
def get_greeting():
    '''Получить приветствие'''
    greeting = base_mdls.AboutCompany.objects.values_list(
        'greeting', flat=True).first()
    return greeting


@sync_to_async
def check_authorization(tg_id=None, email=None):
    '''Проверить авторизацию - наличие тг id'''
    if not tg_id and not email:
        return None

    query = Q()
    if tg_id:
        query |= Q(tg_id=tg_id)
    if email:
        query |= Q(email=email)

    return base_mdls.Client.objects.filter(query).exists()


@sync_to_async
def sign_up(tg_id, name, phone, email):
    '''Зарегистрировать пользователя'''
    new_client = base_mdls.Client.objects.create(
        tg_id=tg_id, name=name, phone=phone, email=email)
    base_mdls.ClientActivity.objects.create(
        name=new_client, last_visit_bot=datetime.now())

    # для демо
    # base_mdls.Master.objects.create(name=new_client)
    # base_mdls.Admin.objects.create(name=new_client)


@sync_to_async
def refresh_tg_id(email, tg_id):
    '''Обновить/добавить тг id в случае входа'''
    client = base_mdls.Client.objects.filter(email=email).first()
    client.tg_id = tg_id
    client.save()


@sync_to_async
def check_promo_on_off():
    '''Проверка включена ли программа лояльности'''
    loyalty_program = add_models.LoyaltyProgram.objects.first()

    # если включен автоматический режим и заполнены таблицы
    # акций, сертификатов, абонементов - и/или
    if loyalty_program.auto_toggle:
        promos = add_models.Promotion.objects.filter(is_active=True).all()
        certificates = add_models.Certificate.objects.filter(
            is_active=True).all()
        abonements = add_models.Abonement.objects.filter(is_active=True).all()

        if promos or certificates or abonements:
            loyalty_program.toggle = True  # активируем промо для клиентов
        else:
            loyalty_program.toggle = False  # деактивируем
        loyalty_program.save()

    return loyalty_program.toggle


@sync_to_async
def check_roles(tg_id):
    '''Проверка роли пользователя'''
    client = base_mdls.Client.objects.filter(tg_id=tg_id).first()
    master = base_mdls.Master.objects.filter(name=client).first()
    admin = base_mdls.Admin.objects.filter(name=client).first()

    if master:
        master = master.is_active_role
    if admin:
        admin = admin.is_active_role

    return master, admin
