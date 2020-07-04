# -*- coding: utf-8 -*-

from django.test import TestCase
try:
    from django.urls import reverse
except ImportError:
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
        self.assertTrue('99.79' in str(response.content) and 'kgs' in str(response.content))

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
        self.assertTrue('220.46' in str(response.content) and 'lbs' in str(response.content))

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
        self.assertTrue('' in str(response.content) and 'kgs' in str(response.content))

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
        self.assertTrue('172.72' in str(response.content) and 'cm' in str(response.content))

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
        self.assertTrue('5' in str(response.content) and 'ft' in str(response.content))
        self.assertTrue('8' in str(response.content) and 'in' in str(response.content))

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
        self.assertTrue('0' in str(response.content) and 'ft' in str(response.content))
        self.assertTrue('0' in str(response.content) and 'in' in str(response.content))
