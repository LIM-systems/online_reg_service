# Generated by Django 5.0 on 2024-10-04 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base_process', '0008_alter_visitjournal_promotion_discount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visitjournal',
            name='create_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата создания записи'),
        ),
    ]
