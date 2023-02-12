from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.places.models import Place
from django.contrib.auth.models import User


class Compilation(models.Model):
    class CompilationType(models.TextChoices):
        PUBLIC = 'PU', _('Public')
        PRIVATE = 'PR', _('Private')

    type = models.CharField(max_length=2, choices=CompilationType.choices, default=CompilationType.PUBLIC)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=1023)
    author = models.ForeignKey(User, on_delete=models.PROTECT)
    gradient = models.JSONField()
    places = models.ManyToManyField(Place)
