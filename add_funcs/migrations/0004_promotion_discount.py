# Generated by Django 5.0 on 2024-10-03 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('add_funcs', '0003_alter_loyaltyprogram_toggle'),
    ]

    operations = [
        migrations.AddField(
            model_name='promotion',
            name='discount',
            field=models.IntegerField(default=123, help_text='Введите процент скидки', verbose_name='Скидка (%)'),
            preserve_default=False,
        ),
    ]