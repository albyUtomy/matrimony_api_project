# Generated by Django 5.1.3 on 2024-11-22 07:30

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserPreference',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caste', models.CharField(blank=True, max_length=50, null=True)),
                ('profession', models.CharField(blank=True, max_length=100, null=True)),
                ('education', models.CharField(blank=True, max_length=100, null=True)),
                ('language', models.CharField(blank=True, max_length=100, null=True)),
                ('age_min', models.PositiveIntegerField(blank=True, help_text='Minimum preferred age.', null=True, validators=[django.core.validators.MinValueValidator(18)])),
                ('age_max', models.PositiveIntegerField(blank=True, help_text='Maximum preferred age.', null=True, validators=[django.core.validators.MinValueValidator(18)])),
                ('income_min', models.PositiveIntegerField(blank=True, null=True)),
                ('income_max', models.PositiveIntegerField(blank=True, null=True)),
                ('height_min', models.PositiveIntegerField(blank=True, null=True)),
                ('height_max', models.PositiveIntegerField(blank=True, null=True)),
                ('is_active', models.BooleanField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='preference', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
