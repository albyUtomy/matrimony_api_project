# Generated by Django 5.1.3 on 2024-11-21 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_profile', '0005_alter_userprofile_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]