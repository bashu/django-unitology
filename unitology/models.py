# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _

from .variables import IMPERIAL, METRIC


class UnitsFieldMixin(models.Model):

    DEFAULT = IMPERIAL
    UNITS = (
        (IMPERIAL, _("Standard (lbs/ft/in)")),
        (METRIC, _("Metric (kg/cm)")),
    )

    units = models.CharField(
        max_length=12, choices=UNITS, default=DEFAULT,
        help_text=_("User specific system of measurements..."),
    )

    class Meta:
        abstract = True
