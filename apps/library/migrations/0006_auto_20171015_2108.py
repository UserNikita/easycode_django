# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-10-15 17:08
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0005_book_page_count'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bookfile',
            old_name='file_format',
            new_name='format',
        ),
        migrations.RenameField(
            model_name='bookfile',
            old_name='file_size',
            new_name='size',
        ),
        migrations.RenameField(
            model_name='bookfile',
            old_name='file_url',
            new_name='url',
        ),
    ]
