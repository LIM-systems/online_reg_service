# base_process/signals.py

from django.db.models.signals import post_migrate
from django.dispatch import receiver
from add_funcs.models import ChatWithAdmin, LoyaltyProgram


@receiver(post_migrate)
def create_chat_with_admin(sender, **kwargs):
    """
    Создаёт запись ChatWithAdmin, если её ещё нет.
    """
    if sender.name == 'add_funcs':
        ChatWithAdmin.objects.get_or_create(pk=1)


@receiver(post_migrate)
def create_chat_with_admin(sender, **kwargs):
    """
    Создаёт запись LoyaltyProgram, если её ещё нет.
    """
    if sender.name == 'add_funcs':
        LoyaltyProgram.objects.get_or_create(pk=1)
