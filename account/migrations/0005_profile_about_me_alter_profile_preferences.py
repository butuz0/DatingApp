# Generated by Django 4.2.4 on 2023-08-05 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_alter_profile_date_of_birth'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='about_me',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='preferences',
            field=models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female'), ('BOTH', 'Male and Female')], max_length=4, null=True),
        ),
    ]
