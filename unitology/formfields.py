# -*- coding: utf-8 -*-

import quantities as pq
from decimal import Decimal, DecimalException

from django import forms
from django.core import validators
from django.core.exceptions import ValidationError
from django.utils.encoding import smart_str
from django.utils import formats

from .conf import settings
from .widgets import (
    WeightWidget, WeightMultiWidget,
    HeightWidget, HeightMultiWidget,
    LengthWidget, LengthMultiWidget,
    SecondsWidget, SecondsMultiWidget,
)
from .utils import convert_weight, convert_length


class UnitsFieldMixin(object):

    def get_units(self):
        return self._units

    def set_units(self, value):
        self._units = self.widget.units = value

    units = property(get_units, set_units)

    @staticmethod
    def conversion(value, from_units, to_units):
        raise NotImplementedError


class BaseField(UnitsFieldMixin, forms.DecimalField):

    def __init__(self, units, *args, **kwargs):
        defaults = {
            'min_value': 0,
        }
        kwargs.update(defaults)
        super(BaseField, self).__init__(*args, **kwargs)
        self.widget.form_class = self.__class__
        self.units = units

    def to_python(self, value):
        if value in validators.EMPTY_VALUES:
            return None
        if self.localize:
            value = formats.sanitize_separators(value)
        value = smart_str(value).strip()
        try:
            value = Decimal(value)
        except DecimalException:
            raise ValidationError(self.error_messages['invalid'])

        return self.conversion(
            value, self.units, settings.UNITOLOGY_DATABASE_UNITS)


class BaseMultiField(UnitsFieldMixin, forms.MultiValueField):

    def __init__(self, units, *args, **kwargs):
        if 'decimal_places' in kwargs.keys():
            del kwargs['decimal_places']
        if 'max_digits' in kwargs.keys():
            del kwargs['max_digits']
        super(BaseMultiField, self).__init__(*args, **kwargs)
        self.widget.form_class = self.__class__
        self.units = units


class WeightField(BaseField):

    def __init__(self, units, *args, **kwargs):
        defaults = {
            'widget': WeightWidget(units=units),
        }
        kwargs.update(defaults)
        super(WeightField, self).__init__(units, *args, **kwargs)

    @staticmethod
    def conversion(value, from_units, to_units):
        try:
            return Decimal(str(convert_weight(value, from_units, to_units))).quantize(Decimal('.01'))
        except ValueError:
            return None


class WeightMultiField(BaseMultiField):

    def __init__(self, units, *args, **kwargs):
        fields = (
            forms.DecimalField(max_digits=10, decimal_places=2, min_value=0),
            forms.CharField(),  # units, i.e. metric, imperial
        )
        defaults = {
            'widget': WeightMultiWidget(units=units),
        }
        kwargs.update(defaults)
        super(WeightMultiField, self).__init__(units, fields, *args, **kwargs)

    def compress(self, data_list):
        if data_list:
            if data_list[0]:
                return self.conversion(
                    data_list[0], data_list[1], settings.UNITOLOGY_DATABASE_UNITS)
        return None

    @staticmethod
    def conversion(value, from_units, to_units):
        try:
            return Decimal(str(convert_weight(value, from_units, to_units))).quantize(Decimal('.01'))
        except ValueError:
            return None


class HeightField(BaseField):

    def __init__(self, units, *args, **kwargs):
        defaults = {
            'widget': HeightWidget(units=units),
        }
        kwargs.update(defaults)
        super(HeightField, self).__init__(units, *args, **kwargs)

    @staticmethod
    def conversion(value, from_units, to_units):
        try:
            return Decimal(str(convert_length(value, from_units, to_units))).quantize(Decimal('.01'))
        except ValueError:
            return None


class HeightMultiField(BaseMultiField):

    def __init__(self, units, *args, **kwargs):
        fields = (
            forms.IntegerField(),
            forms.IntegerField(),
            forms.DecimalField(max_digits=5, decimal_places=2, min_value=0),
        )
        defaults = {
            'widget': HeightMultiWidget(units=units),
        }
        kwargs.update(defaults)
        super(HeightMultiField, self).__init__(units, fields, *args, **kwargs)

    def compress(self, data_list):
        if data_list:
            if data_list[2]:  # return centimeters as is
                return Decimal(data_list[2])
            q = int(data_list[0]) * pq.ft  # convert feet / inches into centimeters
            return self.conversion(
                float(q.rescale(pq.inch) + float(data_list[1]) * pq.inch),
                self.units, settings.UNITOLOGY_DATABASE_UNITS,
            )
        return None

    @staticmethod
    def conversion(value, from_units, to_units):
        try:
            if isinstance(value, (list, tuple)):
                q = int(value[0]) * pq.ft  # convert feet / inches into centimeters
                value = float(q.rescale(pq.inch) + float(value[1]) * pq.inch)
            return Decimal(str(convert_length(value, from_units, to_units))).quantize(Decimal('.01'))
        except ValueError:
            return None


class LengthField(HeightField):

    def __init__(self, units, *args, **kwargs):
        defaults = {
            'widget': LengthWidget(units=units),
        }
        kwargs.update(defaults)
        super(LengthField, self).__init__(units, *args, **kwargs)


class LengthMultiField(HeightMultiField):

    def __init__(self, units, *args, **kwargs):
        fields = (
            forms.IntegerField(),
            forms.IntegerField(),
            forms.DecimalField(max_digits=6, decimal_places=2, min_value=0),
        )
        defaults = {
            'widget': LengthMultiWidget(units=units),
        }
        kwargs.update(defaults)
        super(HeightMultiField, self).__init__(units, fields, *args, **kwargs)


class SecondsField(BaseField):

    def __init__(self, units=None, *args, **kwargs):
        defaults = {
            'widget': SecondsWidget(units=None),
        }
        kwargs.update(defaults)
        super(SecondsField, self).__init__(units, *args, **kwargs)

    @staticmethod
    def conversion(value, from_units, to_units, reverse=False):
        return value  # return raw value


class SecondsMultiField(BaseMultiField):

    def __init__(self, units=None, *args, **kwargs):
        fields = (
            forms.IntegerField(min_value=0),
            forms.IntegerField(min_value=0),
        )
        defaults = {
            'widget': SecondsMultiWidget(units=None),
        }
        kwargs.update(defaults)
        super(SecondsMultiField, self).__init__(units, fields, *args, **kwargs)

    def compress(self, data_list):
        if data_list:  # convert minutes into seconds
            return Decimal(str((int(data_list[0]) * 60) + int(data_list[1])))
        return None

    @staticmethod
    def conversion(value, from_units, to_units, reverse=False):
        return value  # return raw value
