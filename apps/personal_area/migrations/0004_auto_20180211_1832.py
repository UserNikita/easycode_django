# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-02-11 14:32
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('personal_area', '0003_like'),
    ]

    operations = [
        migrations.AlterField(
            model_name='like',
            name='content_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType'),
        ),
        migrations.AlterUniqueTogether(
            name='like',
            unique_together=set([('user', 'object_id', 'content_type')]),
        ),
    ]
