# Generated by Django 5.0 on 2024-10-03 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base_process', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='service',
            name='categories',
        ),
        migrations.AddField(
            model_name='service',
            name='services_categories',
            field=models.ManyToManyField(blank=True, to='base_process.categories', verbose_name='Категории'),
        ),
    ]
