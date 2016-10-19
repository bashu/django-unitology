# -*- coding: utf-8 -*-

import decimal
import quantities as pq

from django.db import models
from django.db.models import signals
from django.utils.functional import curry
from django.utils.translation import ugettext as _

from .conf import settings
from .utils import convert_weight, convert_length


class BaseField(models.DecimalField):
    units = None

    def __init__(self, **kwargs):
        if 'max_digits' in kwargs.keys():
            del kwargs['max_digits']
        if 'decimal_places' in kwargs.keys():
            del kwargs['decimal_places']
        default = kwargs.pop('default', decimal.Decimal('0.00'))  # get "default" or 0.00

        super(BaseField, self).__init__(
            max_digits=10, decimal_places=2, default=default, **kwargs)

    def contribute_to_class(self, cls, name):
        super(BaseField, self).contribute_to_class(cls, name)
        signals.post_init.connect(self._update, cls, True)

    def _update(self, **kwargs):
        self.units = kwargs['instance'].units

    def formfield(self, **kwargs):
        defaults = {
            'units': self.units,
        }
        defaults.update(kwargs)
        return super(BaseField, self).formfield(**defaults)


class WeightField(BaseField):

    def contribute_to_class(self, cls, name):
        super(WeightField, self).contribute_to_class(cls, name)

        def _get_FIELD_display(cls, field):
            if isinstance(field, WeightField):
                value = getattr(cls, field.attname)
                if value:
                    if cls.units != settings.UNITOLOGY_DATABASE_UNITS:
                        weight = round(convert_weight(value, settings.UNITOLOGY_DATABASE_UNITS, cls.units), 2)
                    else:
                        weight = value
                    return '%s %s' % (weight, {'metric': _('kgs'), 'imperial': _('lbs')}.get(cls.units))
                return value
            return super(self.model, cls)._get_FIELD_display(field)
        setattr(cls, '_get_FIELD_display', _get_FIELD_display)

        setattr(cls, 'get_%s_display' % self.name, curry(cls._get_FIELD_display, field=self))

    def formfield(self, **kwargs):
        from unitology import formfields

        defaults = {
            'form_class': formfields.WeightMultiField,
        }
        defaults.update(kwargs)
        return super(WeightField, self).formfield(**defaults)

if 'south' in settings.INSTALLED_APPS:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["^unitology\.fields\.WeightField"])


class HeightField(BaseField):

    def contribute_to_class(self, cls, name):
        super(HeightField, self).contribute_to_class(cls, name)

        def _get_FIELD_display(cls, field):
            if isinstance(field, HeightField):
                value = getattr(cls, field.attname)
                if value:
                    if cls.units != settings.UNITOLOGY_DATABASE_UNITS:
                        value = round(convert_length(value, settings.UNITOLOGY_DATABASE_UNITS, cls.units), 2)
                        q = float(value) * pq.inch  # rescale inches to feet and inches
                        return _('%s ft %s in' % (
                            int(q.rescale(pq.ft)), int(float((q.rescale(pq.ft) % pq.ft).rescale(pq.inch)))))
                    else:
                        return _('%s cm' % value)
                return value
            return super(self.model, cls)._get_FIELD_display(field)
        setattr(cls, '_get_FIELD_display', _get_FIELD_display)

        setattr(cls, 'get_%s_display' % self.name, curry(cls._get_FIELD_display, field=self))

    def formfield(self, **kwargs):
        from unitology import formfields

        defaults = {
            'form_class': formfields.HeightMultiField,
        }
        defaults.update(kwargs)
        return super(HeightField, self).formfield(**defaults)

if 'south' in settings.INSTALLED_APPS:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["^unitology\.fields\.HeightField"])
