from django.db import models


class Place(models.Model):
    name = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    osm_id = models.BigIntegerField()
    osm_type = models.CharField(max_length=255)
    display_name = models.CharField(max_length=1023)
    category = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    address = models.JSONField()

    class Meta:
        unique_together = ['osm_id', 'osm_type', 'category']
