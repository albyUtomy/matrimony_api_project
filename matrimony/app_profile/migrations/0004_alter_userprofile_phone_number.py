# Generated by Django 5.1.3 on 2024-11-21 08:11

import core.validator
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_profile', '0003_userprofile_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='phone_number',
            field=models.CharField(blank=True, help_text='Enter a valid phone number', max_length=10, null=True, unique=True, validators=[core.validator.validate_phone_number]),
        ),
    ]