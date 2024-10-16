from datetime import datetime
from asgiref.sync import sync_to_async
import certifi
from base_process import models as base_mdls
from add_funcs import models as add_mdls


@sync_to_async
def get_about_us_info():
    '''Получить данные о компании'''
    about_us_info = base_mdls.AboutCompany.objects.values_list('name', 'description',
                                                               'image', 'address',
                                                               'work_days', 'work_time', 'phone',).first()
    return about_us_info


@sync_to_async
def get_client_info(tg_id, name=None, phone=None, email=None):
    '''Получить данные о клиенте'''
    client = base_mdls.Client.objects.filter(tg_id=tg_id).first()
    if name:
        client.name = name
    if phone:
        client.phone = phone
    if email:
        client.email = email
    client.save()

    return client


@sync_to_async
def get_future_entries(tg_id):
    '''Получить будущие записи клиента'''
    client = base_mdls.Client.objects.filter(tg_id=tg_id).first()
    now = datetime.now()
    future_entries = base_mdls.VisitJournal.objects.filter(
        visit_client=client,
        visit_date__gt=now
    ).all()

    return future_entries


@sync_to_async
def get_past_entries(tg_id):
    '''Получить прошлые записи клиента'''
    client = base_mdls.Client.objects.filter(tg_id=tg_id).first()
    now = datetime.now()
    past_entries = base_mdls.VisitJournal.objects.filter(
        visit_client=client,
        visit_date__lt=now
    ).all()
    return past_entries


@sync_to_async
def get_loaylity_programs():
    '''Получить данные о лояльности'''
    promos = add_mdls.Promotion.objects.filter(is_active=True).all()
    certificates = add_mdls.Certificate.objects.filter(is_active=True).all()
    abonements = add_mdls.Abonement.objects.filter(is_active=True).all()

    if promos:
        promos = [promo for promo in promos]
    else:
        promos = None

    if certificates:
        certificates = [cert for cert in certificates]
    else:
        certificates = None

    if abonements:
        abonements = [abonement for abonement in abonements]
    else:
        abonements = None

    return promos, certificates, abonements
