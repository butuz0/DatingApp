# Generated by Django 4.2.4 on 2023-08-07 18:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('account', '0007_alter_profile_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('user_from', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='like_user_from', to=settings.AUTH_USER_MODEL)),
                ('user_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='like_user_to', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created'],
                'indexes': [models.Index(fields=['-created'], name='account_lik_created_c48bc8_idx')],
            },
        ),
    ]