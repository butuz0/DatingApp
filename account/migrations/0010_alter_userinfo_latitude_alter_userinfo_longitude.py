# Generated by Django 4.2.4 on 2023-08-12 16:32

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0009_userinfo_delete_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='latitude',
            field=models.FloatField(null=True, validators=[django.core.validators.MaxValueValidator(90), django.core.validators.MinValueValidator(-90)]),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='longitude',
            field=models.FloatField(null=True, validators=[django.core.validators.MaxValueValidator(180), django.core.validators.MinValueValidator(-180)]),
        ),
    ]