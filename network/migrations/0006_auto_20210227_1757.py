# Generated by Django 3.1.6 on 2021-02-27 17:57

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0005_auto_20210227_1756'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='follow',
        ),
        migrations.AddField(
            model_name='user',
            name='follow',
            field=models.ManyToManyField(related_name='userfollow', to=settings.AUTH_USER_MODEL),
        ),
    ]