# Generated by Django 2.2.7 on 2020-04-20 17:26

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('quiz', '0002_quiz_users_passed'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='users',
            field=models.ManyToManyField(blank=True, through='quiz.UserAnswer', to=settings.AUTH_USER_MODEL, verbose_name='Пользователи'),
        ),
    ]
