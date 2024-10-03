from re import search

from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from base_process.models.about_company import AboutCompany
from base_process.models.schedule import MasterSchedule, VisitJournal
from base_process.models.services import Categories, Service
from base_process.models.users import Client, ClientActivity, Master


# клиенты
@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'tg_id', 'comment',)
    list_filter = ('name', 'email')
    search_fields = ('phone', 'tg_id', 'comment',)


# журнал активности клиентов
@admin.register(ClientActivity)
class ClientActivityAdmin(admin.ModelAdmin):
    list_display = ('name', 'last_visit_bot', 'last_visit_web', 'is_blocked',)
    list_filter = ('name', 'is_blocked',)
    search_fields = ('name',)


# мастера
@admin.register(Master)
class MasterAdmin(admin.ModelAdmin):
    list_display = ('name', 'rate', 'photo')
    list_filter = ('rate',)
    search_fields = ('name',)


# категории услуг
@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('name', 'pic')
    list_filter = ('name',)


# услуги
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'duration', 'image', 'price')
    list_filter = ('name', 'duration', 'price')


# график мастеров
@admin.register(MasterSchedule)
class MasterScheduleAdmin(admin.ModelAdmin):
    list_display = ('master', 'date', 'start_time', 'end_time')
    list_filter = ('master', 'date')


# журнал записей и посещений клиентов
@admin.register(VisitJournal)
class VisitJournalAdmin(admin.ModelAdmin):
    list_display = ('visit_client', 'visit_master', 'visit_date', 'create_date',
                    'visit_service', 'confirmation',
                    'cancel', 'finish', 'rate', 'comment', 'note',)
    list_filter = ('visit_client', 'visit_master', 'visit_date', 'create_date',
                   'visit_service', 'confirmation',
                   'cancel', 'finish', 'rate', 'comment', 'note',)


# о компании
@admin.register(AboutCompany)
class AboutCompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'preview_logo_mini', 'preview_image_mini',
                    'greeting', 'address', 'work_days', 'work_time', 'phone',)
    readonly_fields = ('preview_logo', 'preview_image')

    def has_add_permission(self, request):
        """Запрещает добавление новых записей, если запись уже существует."""
        return not AboutCompany.objects.exists()

    def has_delete_permission(self, request, obj=None):
        """Запрещает удаление записей."""
        return False

    @admin.display(description='Превью')
    def preview_logo(self, obj):
        '''Превью фото лого в админке'''
        return mark_safe(
            f'<img src="{obj.logo.url}" style="max-height: 300px;">')

    @admin.display(description='Превью')
    def preview_logo_mini(self, obj):
        '''Превью фото лого в админке'''
        return mark_safe(
            f'<img src="{obj.logo.url}" style="max-width: 100px;">')

    @admin.display(description='Превью')
    def preview_image(self, obj):
        '''Превью фото компании в админке'''
        return mark_safe(
            f'<img src="{obj.image.url}" style="max-height: 300px;">')

    @admin.display(description='Превью')
    def preview_image_mini(self, obj):
        '''Превью фото компании в админке'''
        return mark_safe(
            f'<img src="{obj.image.url}" style="max-width: 100px;">')
