# Generated by Django 2.1.3 on 2018-11-05 18:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0013_auto_20180901_2235'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='color',
            field=models.PositiveIntegerField(choices=[(0, 'bgm-white'), (1, 'bgm-black'), (2, 'bgm-brown'), (3, 'bgm-pink'), (4, 'bgm-red'), (5, 'bgm-blue'), (6, 'bgm-purple'), (7, 'bgm-deeppurple'), (8, 'bgm-lightblue'), (9, 'bgm-cyan'), (10, 'bgm-teal'), (11, 'bgm-green'), (12, 'bgm-lightgreen'), (13, 'bgm-lime'), (14, 'bgm-yellow'), (15, 'bgm-amber'), (16, 'bgm-orange'), (17, 'bgm-deeporange'), (18, 'bgm-gray'), (19, 'bgm-bluegray'), (20, 'bgm-indigo')], default=8, verbose_name='Цвет'),
        ),
    ]
