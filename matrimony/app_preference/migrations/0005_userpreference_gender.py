# Generated by Django 5.1.3 on 2024-11-24 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_preference', '0004_remove_userpreference_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userpreference',
            name='gender',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
