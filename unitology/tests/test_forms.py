# -*- coding: utf-8 -*-

from decimal import Decimal
from django.test import TestCase

from django_dynamic_fixture import N

from unitology.models import UnitsFieldMixin
from unitology.forms import UnitsFieldFormMixin
from unitology.variables import IMPERIAL, METRIC
from unitology.fields import WeightField, HeightField


class ModelF(UnitsFieldMixin):

    weight = WeightField(blank=True, null=True)
    height = HeightField(blank=True, null=True)


class ModelForm(UnitsFieldFormMixin):

    class Meta:
        model = ModelF
        fields = ['weight', 'height']


class UnitsFieldFormTest(TestCase):

    model_info = {
        'weight': 66,
        'height': 175,
        }

    def setUp(self):
        self.model = N(ModelF, **self.model_info)

    def test_default(self): # imperial is default
        form = ModelForm(instance=self.model)
        self.assertTrue('145.51' in form.as_p() and '"%s" selected' % IMPERIAL in form.as_p())

        self.assertTrue('"5" selected' in form.as_p() and 'ft' in form.as_p())
        self.assertTrue('"8" selected' in form.as_p() and 'in' in form.as_p())
        self.assertTrue('175' in form.as_p() and 'cm' in form.as_p())

    def test_metric_system(self):
        self.model.units = METRIC

        form = ModelForm(instance=self.model)
        self.assertTrue('66' in form.as_p() and '"%s" selected' % METRIC in form.as_p())

        self.assertTrue('"5" selected' in form.as_p() and 'ft' in form.as_p())
        self.assertTrue('"8" selected' in form.as_p() and 'in' in form.as_p())
        self.assertTrue('175' in form.as_p() and 'cm' in form.as_p())

    def test_success_case(self):
        data = {
            'units': 'imperial',
            'weight_0': '145',
            'weight_1': 'imperial',
            'height_ft': '5',
            'height_in': '8',
            }
        form = ModelForm(data=data, instance=self.model)
        self.failUnless(form.is_valid())

        self.assertEqual(self.model.weight, Decimal('65.77'))
        self.assertEqual(self.model.height, Decimal('172.72'))
