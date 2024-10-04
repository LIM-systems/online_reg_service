# Generated by Django 5.0 on 2024-10-03 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('add_funcs', '0004_promotion_discount'),
        ('base_process', '0003_visitjournal_promotion_discount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='visitjournal',
            name='promotion_discount',
        ),
        migrations.AddField(
            model_name='visitjournal',
            name='promotion_discount',
            field=models.ManyToManyField(to='add_funcs.promotion', verbose_name='Акция'),
        ),
    ]