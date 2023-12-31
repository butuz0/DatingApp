# Generated by Django 4.2.4 on 2023-08-05 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_alter_profile_date_of_birth_alter_profile_gender_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='date_of_birth',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='gender',
            field=models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female')], max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='users/%Y/%m/%d/'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='preferences',
            field=models.CharField(blank=True, max_length=4, null=True),
        ),
    ]
