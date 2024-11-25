# Generated by Django 5.1.3 on 2024-11-24 23:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_message', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='status',
            field=models.CharField(choices=[('unseen', 'Unseen'), ('seen', 'Seen')], default='unseen', max_length=10),
        ),
    ]
