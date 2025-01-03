# Generated by Django 5.1.3 on 2024-11-24 22:40

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_matching', '0003_alter_matching_unique_together'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='matching',
            unique_together=set(),
        ),
        migrations.AlterField(
            model_name='matching',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='matches_initiated', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='MatchDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('matched_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('matching', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_matching.matching')),
            ],
            options={
                'unique_together': {('matching', 'matched_user')},
            },
        ),
        migrations.AddField(
            model_name='matching',
            name='matched_users',
            field=models.ManyToManyField(related_name='matches_received', through='app_matching.MatchDetail', to=settings.AUTH_USER_MODEL),
        ),
        migrations.RemoveField(
            model_name='matching',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='matching',
            name='matched_user',
        ),
        migrations.RemoveField(
            model_name='matching',
            name='score',
        ),
        migrations.RemoveField(
            model_name='matching',
            name='updated_at',
        ),
    ]
