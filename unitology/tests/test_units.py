# -*- coding: utf-8 -*-

from django.test import TestCase

from unitology import utils
from unitology.variables import IMPERIAL, METRIC


class UtilsTest(TestCase):

    def test_kg2lb(self):
        self.assertEqual(round(utils.kg2lb(100), 1), 220.5)

    def test_lb2kg(self):
        self.assertEqual(round(utils.lb2kg(220.5), 1), 100.0)

    def test_cm2in(self):
        self.assertEqual(round(utils.cm2in(175), 1), 68.9)

    def test_in2cm(self):
        self.assertEqual(round(utils.in2cm(68.9), 1), 175.0)

    def test_convert_weight(self):
        self.assertEqual(round(utils.convert_weight(100, METRIC, IMPERIAL), 1), 220.5)
        self.assertEqual(round(utils.convert_weight(220.5, IMPERIAL, METRIC), 1), 100.0)

    def test_convert_length(self):
        self.assertEqual(round(utils.convert_length(175, METRIC, IMPERIAL), 1), 68.9)
        self.assertEqual(round(utils.convert_length(68.9, IMPERIAL, METRIC), 1), 175.0)
