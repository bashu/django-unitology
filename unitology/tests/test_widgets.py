# -*- coding: utf-8 -*-

from decimal import Decimal

from django.test import TestCase

from unitology.formfields import *
from unitology.widgets import *
from unitology.variables import IMPERIAL, METRIC


class WeightFieldTest(TestCase):

    def test_imperial_field(self):
        self.field = WeightField(units=IMPERIAL)

        response = self.field.widget.render('weight', 220, {'id': 'id_weight'})
        self.assertTrue('220' in response and 'lbs' in response)

        self.assertEqual(self.field.to_python(220), Decimal('99.79'))

    def test_metric_field(self):
        self.field = WeightField(units=METRIC)

        response = self.field.widget.render('weight', 100, {'id': 'id_weight'})
        self.assertTrue('100' in response and 'kgs' in response)

        self.assertEqual(self.field.to_python(100), Decimal('100'))


class WeightMultiFieldTest(TestCase):

    def test_imperial_field(self):
        self.field = WeightMultiField(units=IMPERIAL)
        self.assertEqual(self.field.widget.decompress(100), ('220.46', IMPERIAL))

        response = self.field.widget.render('weight', [220, IMPERIAL], {'id': 'id_weight'})
        self.assertTrue('220' in response and 'lbs' in response)

        self.assertEqual(self.field.compress([220, IMPERIAL]), Decimal('99.79'))

    def test_metric_field(self):
        self.field = WeightMultiField(units=METRIC)
        self.assertEqual(self.field.widget.decompress(100), ('100.00', METRIC))

        response = self.field.widget.render('weight', [100, METRIC], {'id': 'id_weight'})
        self.assertTrue('100' in response and 'kgs' in response)

        self.assertEqual(self.field.compress([100, METRIC]), Decimal('100'))


class HeightFieldTest(TestCase):

    def test_imperial_field(self):
        self.field = HeightField(units=IMPERIAL)

        response = self.field.widget.render('height', 68.89, {'id': 'id_height'})
        self.assertTrue('68.89' in response and 'ft/in' in response)

        self.assertEqual(self.field.to_python(68.89), Decimal('174.98'))

    def test_metric_field(self):
        self.field = HeightField(units=METRIC)

        response = self.field.widget.render('height', 175, {'id': 'id_height'})
        self.assertTrue('175' in response and 'cm' in response)

        self.assertEqual(self.field.to_python(175), Decimal('175'))


class HeightMultiFieldTest(TestCase):

    def test_imperial_field(self):
        self.field = HeightMultiField(units=IMPERIAL)
        self.assertEqual(self.field.widget.decompress('175'), (5, 8, '175'))

        response = self.field.widget.render('height', [5, 8, '175'], {'id': 'id_height'})
        self.assertTrue('5' in response and 'ft' in response)
        self.assertTrue('8' in response and 'in' in response)
        
        self.assertEqual(self.field.compress([5, 8, None]), Decimal('172.72'))

    def test_metric_field(self):
        self.field = HeightMultiField(units=METRIC)
        self.assertEqual(self.field.widget.decompress('175'), (5, 8, '175'))

        response = self.field.widget.render('height', [5, 8, '175'], {'id': 'id_height'})
        self.assertTrue('175' in response and 'cm' in response)

        self.assertEqual(self.field.compress([None, None, '175']), Decimal('175'))


class SecondsFieldTest(TestCase):

    def test_default(self):
        self.field = SecondsField()

        response = self.field.widget.render('seconds', 100, {'id': 'id_seconds'})
        self.assertTrue('100' in response and 'sec' in response)

        self.assertEqual(self.field.to_python(100), Decimal('100'))


class SecondsMultiFieldTest(TestCase):

    def test_default(self):
        self.field = SecondsMultiField()
        self.assertEqual(self.field.widget.decompress('100'), ('1', '40'))

        response = self.field.widget.render('seconds', [1, 40], {'id': 'id_seconds'})
        self.assertTrue('1' in response and 'min' in response)
        self.assertTrue('40' in response and 'sec' in response)

        self.assertEqual(self.field.compress(['1', '40']), Decimal('100'))
