# -*- coding: utf-8 -*-

from django.test import TestCase

from django_dynamic_fixture import N

from unitology.models import UnitsFieldMixin
from unitology.variables import IMPERIAL, METRIC
from unitology.fields import WeightField, HeightField


class ModelM(UnitsFieldMixin):

    weight = WeightField(blank=True, null=True)
    height = HeightField(blank=True, null=True)


class UnitsFieldTest(TestCase):

    model_info = {
        'weight': 66,
        'height': 175,
    }

    def setUp(self):
        self.model = N(ModelM, **self.model_info)

    def test_default(self):  # imperial is default
        self.assertEqual(self.model.units, IMPERIAL)
        self.assertEqual(self.model.get_height_display(), '5 ft 8 in')
        self.assertEqual(self.model.get_weight_display(), '145.51 lbs')

    def test_metric_system(self):
        self.model.units = METRIC

        self.assertEqual(self.model.units, METRIC)
        self.assertEqual(self.model.get_height_display(), '175 cm')
        self.assertEqual(self.model.get_weight_display(), '66 kgs')
