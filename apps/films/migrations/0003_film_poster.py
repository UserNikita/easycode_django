# Generated by Django 4.1 on 2025-01-29 21:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('films', '0002_film_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='film',
            name='poster',
            field=models.URLField(blank=True, null=True, verbose_name='Ссылка на постер'),
        ),
    ]
