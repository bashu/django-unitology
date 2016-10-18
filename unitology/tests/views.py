# -*- coding: utf-8 -*-

from django.test import TestCase
from django.core.urlresolvers import reverse

from unitology.variables import IMPERIAL, METRIC


class ReloadViewTest(TestCase):

    def test_weight_multi_field(self):
        data = {
            'from_units': IMPERIAL,
            'to_units': METRIC,
            'id': 'id_weight',
            'name': 'weight',
            'value': '220',
            'module_name': 'unitology.formfields',
            'klass_name': 'WeightMultiField'
        }

        response = self.client.get(reverse('unitology_reload'), data, **{
                'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue('99.79' in response.content and 'kgs' in response.content)

        data = {
            'from_units': METRIC,
            'to_units': IMPERIAL,
            'id': 'id_weight',
            'name': 'weight',
            'value': '100',
            'module_name': 'unitology.formfields',
            'klass_name': 'WeightMultiField'
        }

        response = self.client.get(reverse('unitology_reload'), data, **{
                'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue('220.46' in response.content and 'lbs' in response.content)

        # pass incorrect value
        data = {
            'from_units': IMPERIAL,
            'to_units': METRIC,
            'id': 'id_weight',
            'name': 'weight',
            'value': 'qwetry',
            'module_name': 'unitology.formfields',
            'klass_name': 'WeightMultiField'
        }

        response = self.client.get(reverse('unitology_reload'), data, **{
                'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue('' in response.content and 'kgs' in response.content)

    def test_height_multi_field(self):
        data = {
            'from_units': IMPERIAL,
            'to_units': METRIC,
            'id': 'id_height',
            'name': 'height',
            'value[]': ['5', '8'],
            'module_name': 'unitology.formfields',
            'klass_name': 'HeightMultiField'
        }

        response = self.client.get(reverse('unitology_reload'), data, **{
                'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue('172.72' in response.content and 'cm' in response.content)

        data = {
            'from_units': METRIC,
            'to_units': IMPERIAL,
            'id': 'id_height',
            'name': 'height',
            'value': '175',
            'module_name': 'unitology.formfields',
            'klass_name': 'HeightMultiField'
        }

        response = self.client.get(reverse('unitology_reload'), data, **{
                'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue('5' in response.content and 'ft' in response.content)
        self.assertTrue('8' in response.content and 'in' in response.content)

        # pass incorrect value
        data = {
            'from_units': METRIC,
            'to_units': IMPERIAL,
            'id': 'id_height',
            'name': 'height',
            'value[]': 'qwerty',
            'module_name': 'unitology.formfields',
            'klass_name': 'HeightMultiField'
        }

        response = self.client.get(reverse('unitology_reload'), data, **{
                'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue('0' in response.content and 'ft' in response.content)
        self.assertTrue('0' in response.content and 'in' in response.content)
