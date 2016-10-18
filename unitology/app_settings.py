# -*- coding: utf-8 -*-

from django.conf import settings

from .variables import METRIC

# all values will be converted ...
DATABASE_UNITS = getattr(settings, 'UNITOLOGY_DATABASE_UNITS', METRIC)
