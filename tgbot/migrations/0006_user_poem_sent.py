# Generated by Django 3.2.4 on 2021-06-19 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tgbot', '0005_alter_favourite_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='poem_sent',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]