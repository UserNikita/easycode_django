# Generated by Django 2.1.3 on 2019-03-15 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assay', '0002_answer_correct'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категирии',
            },
        ),
    ]