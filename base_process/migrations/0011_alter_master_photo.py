# Generated by Django 5.0 on 2024-10-09 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base_process', '0010_alter_service_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='master',
            name='photo',
            field=models.ImageField(default='masters/default.png', upload_to='masters/', verbose_name='Фото мастера'),
        ),
    ]
