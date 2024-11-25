# Generated by Django 5.1.3 on 2024-11-25 00:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_connection_handler', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friendrequest',
            name='status',
            field=models.CharField(choices=[('sent', 'Sent'), ('accepted', 'Accepted'), ('rejected', 'Rejected'), ('blocked', 'Blocked'), ('pending', 'Pending')], default='sent', max_length=10),
        ),
    ]
