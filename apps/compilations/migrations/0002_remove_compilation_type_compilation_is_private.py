# Generated by Django 4.1.6 on 2023-02-12 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compilations', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='compilation',
            name='type',
        ),
        migrations.AddField(
            model_name='compilation',
            name='is_private',
            field=models.BooleanField(default=False),
        ),
    ]
