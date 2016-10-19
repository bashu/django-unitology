# -*- coding: utf-8 -*-

from django.conf import settings  # pylint: disable=W0611

from appconf import AppConf

from .variables import METRIC


class UnitologySettings(AppConf):
    DATABASE_UNITS = METRIC

    class Meta:
        prefix = 'unitology'
        holder = 'unitology.conf.settings'
