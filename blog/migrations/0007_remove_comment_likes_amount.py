# Generated by Django 4.2.4 on 2024-05-17 15:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_remove_post_likes_amount_comment_likes_amount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='likes_amount',
        ),
    ]
