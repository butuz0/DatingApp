# Generated by Django 4.2.4 on 2023-12-19 23:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0015_alter_interest_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='about_me',
            field=models.TextField(max_length=250, null=True),
        ),
    ]
