# Generated by Django 4.1.6 on 2023-02-12 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('osm_id', models.BigIntegerField()),
                ('osm_type', models.CharField(max_length=255)),
                ('display_name', models.CharField(max_length=1023)),
                ('category', models.CharField(max_length=255)),
                ('type', models.CharField(max_length=255)),
                ('address', models.JSONField()),
            ],
            options={
                'unique_together': {('osm_id', 'osm_type', 'category')},
            },
        ),
    ]