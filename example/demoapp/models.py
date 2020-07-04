from django.db import models

from unitology.models import UnitsFieldMixin
from unitology.fields import WeightField, HeightField


class Person(UnitsFieldMixin):

    name = models.CharField(max_length=128)

    weight = WeightField(blank=True, null=True)
    height = HeightField(blank=True, null=True)

    class Meta:
        pass

    def __str__(self):
        return self.name
