# Generated by Django 4.2.4 on 2023-08-16 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conversations', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='message_read',
            field=models.BooleanField(default=False),
        ),
    ]