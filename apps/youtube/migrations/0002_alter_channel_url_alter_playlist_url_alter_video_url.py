# Generated by Django 4.1 on 2024-11-09 23:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('youtube', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='channel',
            name='url',
            field=models.URLField(unique=True, verbose_name='Url'),
        ),
        migrations.AlterField(
            model_name='playlist',
            name='url',
            field=models.URLField(unique=True, verbose_name='Url'),
        ),
        migrations.AlterField(
            model_name='video',
            name='url',
            field=models.URLField(unique=True, verbose_name='Url'),
        ),
    ]
