# Generated by Django 4.2.4 on 2023-12-09 12:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('account', '0010_alter_userinfo_latitude_alter_userinfo_longitude'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupOfInterests',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Interest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.groupofinterests')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=2, null=True)),
                ('date_of_birth', models.DateField(null=True)),
                ('photo', models.ImageField(null=True, upload_to='users/%Y/%m/%d/')),
                ('gender_preference', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('BOTH', 'Male and Female')], max_length=4, null=True)),
                ('about_me', models.TextField(null=True)),
                ('interests', models.ManyToManyField(to='account.interest')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_info', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='UserInfo',
        ),
    ]