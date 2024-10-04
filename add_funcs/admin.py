from django.contrib import admin

from add_funcs.models import (Abonement, AbonementsJournal, Certificate,
                              CertificatesJournal, ChatWithAdmin,
                              LoyaltyProgram, Promotion)


# акции
@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ('name', 'discount', 'image', 'is_active')
    list_filter = ('is_active', 'discount')
    search_fields = ('name',)
    list_per_page = 50


# сертификаты
@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('name', 'period', 'image', 'is_active')
    list_filter = ('is_active', 'period')
    search_fields = ('name',)
    list_per_page = 50


# абонементы
@admin.register(Abonement)
class AbonementAdmin(admin.ModelAdmin):
    list_display = ('name', 'period', 'image', 'is_active')
    list_filter = ('is_active', 'period')
    search_fields = ('name',)
    list_per_page = 50


# журнал покупок абонементов
@admin.register(AbonementsJournal)
class AbonementsJournalAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'purchased_abonement', 'date_time',)
    list_filter = ('purchased_abonement', 'date_time')
    search_fields = ('client_name', 'purchased_abonement')
    readonly_fields = ('date_time',)
    list_per_page = 50


# журнал покупок сертификатов
@admin.register(CertificatesJournal)
class CertificatesJournalAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'purchased_certificate', 'date_time',)
    list_filter = ('purchased_certificate', 'date_time')
    search_fields = ('client_name', 'purchased_certificate')
    readonly_fields = ('date_time',)
    list_per_page = 50


# чат с админом
@admin.register(ChatWithAdmin)
class ChatWithAdminAdmin(admin.ModelAdmin):
    list_display = ('is_active',)

    def has_add_permission(self, request):
        """Запрещает добавление новых записей, если запись уже существует."""
        return not ChatWithAdmin.objects.exists()

    def has_delete_permission(self, request, obj=None):
        """Запрещает удаление записей."""
        return False


# программа лояльности
@admin.register(LoyaltyProgram)
class LoyaltyProgramAdmin(admin.ModelAdmin):
    list_display = ('auto_toggle', 'toggle',)

    def has_add_permission(self, request):
        """Запрещает добавление новых записей, если запись уже существует."""
        return not LoyaltyProgram.objects.exists()

    def has_delete_permission(self, request, obj=None):
        """Запрещает удаление записей."""
        return False
