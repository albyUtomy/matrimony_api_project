# Generated by Django 5.1.3 on 2024-11-20 18:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_admin', '0002_remove_categoryvalue_id_categoryvalue_value_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='categoryvalue',
            old_name='category_id',
            new_name='category',
        ),
    ]
