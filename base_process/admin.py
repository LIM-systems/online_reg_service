from re import search

from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from base_process.models.about_company import AboutCompany
from base_process.models.schedule import MasterSchedule, VisitJournal
from base_process.models.services import Categories, Service
from base_process.models.users import Admin, Client, ClientActivity, Master


# клиенты
@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'tg_id', 'comment',)
    list_filter = ('name', 'email')
    search_fields = ('phone', 'tg_id', 'comment',)
    readonly_fields = ('tg_id',)


# журнал активности клиентов
@admin.register(ClientActivity)
class ClientActivityAdmin(admin.ModelAdmin):
    list_display = ('name', 'last_visit_bot', 'last_visit_web', 'is_blocked',)
    list_filter = ('name', 'is_blocked',)
    search_fields = ('name',)
    readonly_fields = ('name', 'last_visit_bot',
                       'last_visit_web', 'is_blocked',)


# мастера
@admin.register(Master)
class MasterAdmin(admin.ModelAdmin):
    list_display = ('name', 'rate', 'preview_photo_mini')
    list_filter = ('rate',)
    search_fields = ('name',)
    readonly_fields = ('rate', 'preview_photo')

    @admin.display(description='Превью')
    def preview_photo(self, obj):
        '''Превью фото мастера в админке'''
        if obj.photo:
            return mark_safe(
                f'<img src="{obj.photo.url}" style="max-height: 300px;">')
        return '-'

    @admin.display(description='Превью')
    def preview_photo_mini(self, obj):
        '''Превью фото мастера в админке'''
        if obj.photo:
            return mark_safe(
                f'<img src="{obj.photo.url}" style="max-width: 100px;">')
        return '-'


# категории услуг
@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('name', 'pic')
    list_filter = ('name',)


# услуги
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'duration', 'preview_image_mini', 'price')
    list_filter = ('name', 'duration', 'price')
    readonly_fields = ('preview_image',)

    @admin.display(description='Превью')
    def preview_image(self, obj):
        '''Превью иконка услуги в админке'''
        if obj.image:
            return mark_safe(
                f'<img src="{obj.image.url}" style="max-height: 300px;">')
        return "-"

    @admin.display(description='Превью')
    def preview_image_mini(self, obj):
        '''Превью иконка услуги в админке'''
        if obj.image:
            return mark_safe(
                f'<img src="{obj.image.url}" style="max-width: 100px;">')
        return "-"


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
    readonly_fields = ('create_date',)


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

    @admin.display(description='Превью лого')
    def preview_logo(self, obj):
        '''Превью фото лого в админке'''
        if obj.logo:
            return mark_safe(
                f'<img src="{obj.logo.url}" style="max-height: 300px;">')
        return '-'

    @admin.display(description='Превью лого')
    def preview_logo_mini(self, obj):
        '''Превью фото лого в админке'''
        if obj.logo:
            return mark_safe(
                f'<img src="{obj.logo.url}" style="max-width: 100px;">')
        return '-'

    @admin.display(description='Превью фото копании')
    def preview_image(self, obj):
        '''Превью фото компании в админке'''
        if obj.image:
            return mark_safe(
                f'<img src="{obj.image.url}" style="max-height: 300px;">')
        return '-'

    @admin.display(description='Превью фото компании')
    def preview_image_mini(self, obj):
        '''Превью фото компании в админке'''
        if obj.image:
            return mark_safe(
                f'<img src="{obj.image.url}" style="max-width: 100px;">')
        return '-'


# администраторы
@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)
