# Generated by Django 4.2.4 on 2023-12-18 21:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0014_groupofinterests_background_color'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interest',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='interests', to='account.groupofinterests'),
        ),
    ]