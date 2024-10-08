# Generated by Django 5.1.1 on 2024-10-03 10:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('base_process', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Abonement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название акции')),
                ('description', models.TextField(blank=True, verbose_name='Описание')),
                ('image', models.ImageField(blank=True, null=True, upload_to='promotions/', verbose_name='Картинка акции')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активна')),
                ('period', models.IntegerField(blank=True, help_text='Введите количество дней', null=True, verbose_name='Период (дни)')),
            ],
            options={
                'verbose_name': 'Абонемент',
                'verbose_name_plural': 'Абонементы',
            },
        ),
        migrations.CreateModel(
            name='Certificate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название акции')),
                ('description', models.TextField(blank=True, verbose_name='Описание')),
                ('image', models.ImageField(blank=True, null=True, upload_to='promotions/', verbose_name='Картинка акции')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активна')),
                ('period', models.IntegerField(blank=True, help_text='Введите количество дней', null=True, verbose_name='Период (дни)')),
            ],
            options={
                'verbose_name': 'Сертификат',
                'verbose_name_plural': 'Сертификаты',
            },
        ),
        migrations.CreateModel(
            name='ChatWithAdmin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Чат с админом',
                'verbose_name_plural': 'Чат с админом',
            },
        ),
        migrations.CreateModel(
            name='Promotion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название акции')),
                ('description', models.TextField(blank=True, verbose_name='Описание')),
                ('image', models.ImageField(blank=True, null=True, upload_to='promotions/', verbose_name='Картинка акции')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активна')),
                ('date_start', models.DateTimeField(blank=True, null=True, verbose_name='Дата начала')),
                ('date_end', models.DateTimeField(blank=True, null=True, verbose_name='Дата окончания')),
            ],
            options={
                'verbose_name': 'Акция',
                'verbose_name_plural': 'Акции',
            },
        ),
        migrations.CreateModel(
            name='AbonementsJournal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_time', models.DateTimeField(auto_now_add=True, verbose_name='Дата покупки')),
                ('client_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base_process.client', verbose_name='Клиент')),
                ('purchased_abonement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='add_funcs.abonement', verbose_name='Акция')),
            ],
            options={
                'verbose_name': 'Журнал покупок абонементов',
                'verbose_name_plural': 'Журнал покупок абонементов',
            },
        ),
        migrations.CreateModel(
            name='CertificatesJournal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_time', models.DateTimeField(auto_now_add=True, verbose_name='Дата покупки')),
                ('client_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base_process.client', verbose_name='Клиент')),
                ('purchased_certificate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='add_funcs.certificate', verbose_name='Сертификат')),
            ],
            options={
                'verbose_name': 'Журнал покупок сертификатов',
                'verbose_name_plural': 'Журнал покупок сертификатов',
            },
        ),
    ]
