# Generated by Django 3.1.6 on 2021-02-27 16:06

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0002_remove_user_followers'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='following',
        ),
        migrations.AddField(
            model_name='user',
            name='follow',
            field=models.ManyToManyField(related_name='userfollow', to=settings.AUTH_USER_MODEL),
        ),
    ]
