# Generated by Django 5.1.3 on 2024-11-22 10:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_preference', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userpreference',
            name='income_max',
        ),
        migrations.RemoveField(
            model_name='userpreference',
            name='income_min',
        ),
    ]