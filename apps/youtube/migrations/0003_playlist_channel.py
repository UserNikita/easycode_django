# Generated by Django 4.1 on 2024-11-09 23:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('youtube', '0002_alter_channel_url_alter_playlist_url_alter_video_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='playlist',
            name='channel',
            field=models.ForeignKey(default=66, on_delete=django.db.models.deletion.CASCADE, to='youtube.channel', verbose_name='Канал'),
            preserve_default=False,
        ),
    ]