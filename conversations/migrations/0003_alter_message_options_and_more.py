# Generated by Django 4.2.4 on 2023-08-16 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conversations', '0002_message_message_read'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ['created_at']},
        ),
        migrations.RemoveIndex(
            model_name='message',
            name='conversatio_created_aa6dd8_idx',
        ),
        migrations.AddIndex(
            model_name='message',
            index=models.Index(fields=['created_at'], name='conversatio_created_792fff_idx'),
        ),
    ]
