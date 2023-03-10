# Generated by Django 4.1.6 on 2023-02-12 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='place',
            unique_together=set(),
        ),
        migrations.AddConstraint(
            model_name='place',
            constraint=models.UniqueConstraint(fields=('osm_id', 'osm_type', 'category'), name='place_osm_identificators'),
        ),
    ]
