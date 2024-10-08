from asgiref.sync import sync_to_async

from base_process import models as base_mdls


@sync_to_async
def get_greeting():
    '''Получить приветствие'''
    greeting = base_mdls.AboutCompany.objects.values_list(
        'greeting', flat=True).first()
    return greeting


@sync_to_async
def check_authorization(tg_id):
    '''Проверить авторизацию'''
    return base_mdls.Client.objects.filter(tg_id=tg_id).exists()


@sync_to_async
def sign_up(tg_id, name, phone, email):
    '''Зарегистрировать пользователя'''
    base_mdls.Client.objects.create(
        tg_id=tg_id, name=name, phone=phone, email=email)
