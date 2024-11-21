# Generated by Django 5.1.3 on 2024-11-21 09:13

import core.validator
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_user_authentications', '0009_usersetupmodel_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersetupmodel',
            name='phone_no',
            field=models.CharField(help_text='Enter a valid phone number', max_length=10, unique=True, validators=[core.validator.validate_phone_number]),
        ),
    ]
