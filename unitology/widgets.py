# -*- coding: utf-8 -*-

import os
import quantities as pq

from django import forms
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _

from .conf import settings
from .variables import IMPERIAL, METRIC


class BaseWidget(forms.TextInput):

    def __init__(self, units, *args, **kwargs):
        super(BaseWidget, self).__init__(*args, **kwargs)
        self.units = units

    def render(self, name, value, attrs=None):
        return render_to_string(self.get_template_name(self.units), {
            'widget': super(BaseWidget, self).render(name, value, attrs),
        })

    def get_template_name(self, postfix=None):
        if postfix is not None:
            filepath, filename = os.path.split(self.template_name)
            basename, ext = os.path.splitext(filename)
            return os.path.join(filepath, '%s_%s%s' % (basename, postfix, ext))
        return self.template_name


class BaseMultiWidget(forms.MultiWidget):

    def __init__(self, units, widgets, attrs=None):
        super(BaseMultiWidget, self).__init__(widgets, attrs)
        self.units = units


class WeightWidget(BaseWidget):
    template_name = 'unitology/weight_field.html'


class WeightMultiWidget(BaseMultiWidget):
    template_name = 'unitology/weight_multi_field.html'

    def __init__(self, units, attrs=None):
        widgets = (
            forms.TextInput(attrs=attrs),
            forms.Select(attrs=attrs, choices=((IMPERIAL, _("lbs")), (METRIC, _("kgs")))),
        )
        super(WeightMultiWidget, self).__init__(units, widgets, attrs)

    def decompress(self, value):
        if value:
            if isinstance(value, (list, tuple)):
                return tuple(value)
            return (str(self.form_class.conversion(value, settings.UNITOLOGY_DATABASE_UNITS, self.units)), self.units)
        return (None, self.units)

    def render(self, name, value, attrs=None):
        if self.is_localized:
            for widget in self.widgets:
                widget.is_localized = self.is_localized
        # value is a list of values, each corresponding to a widget
        # in self.widgets.
        if not isinstance(value, list):
            value = self.decompress(value)
        output = []
        final_attrs = self.build_attrs(attrs)
        id_ = final_attrs.get('id', None)

        for i, widget in enumerate(self.widgets):
            try:
                widget_value = value[i]
            except IndexError:
                widget_value = None
            if id_:
                final_attrs = dict(final_attrs, id='%s_%s' % (id_, i))
            output.append(widget.render(name + '_%s' % i, widget_value, final_attrs))

        return render_to_string(self.template_name, {
            'id': id_,
            'name': name,
            'widget': mark_safe(self.format_output(output)),
            'module_name': str(self.form_class.__module__),
            'klass_name': self.form_class.__name__,
        })

    def format_output(self, rendered_widgets):
        return "%s&nbsp;%s" % (rendered_widgets[0], rendered_widgets[1])


class HeightWidget(BaseWidget):
    template_name = 'unitology/height_field.html'


class HeightMultiWidget(BaseMultiWidget):
    template_name = 'unitology/height_multi_field.html'

    none_value = ('', '---')

    def __init__(self, units, attrs=None):
        widgets = (
            forms.Select(attrs=attrs, choices=[(v, str(v)) for v in range(8, 2, -1)]),
            forms.Select(attrs=attrs, choices=[(v, str(v)) for v in range(0, 12)]),
            forms.TextInput(attrs=attrs),
        )
        super(HeightMultiWidget, self).__init__(units, widgets, attrs)

        if not self.is_required:
            for w in self.widgets:
                if isinstance(w, forms.Select):
                    w.choices.insert(0, self.none_value)

    def decompress(self, value):
        if value:
            if isinstance(value, (list, tuple)):
                return tuple(value)
            try:
                # rescale inches to feet and inches
                q = float(self.form_class.conversion(value, settings.UNITOLOGY_DATABASE_UNITS, IMPERIAL)) * pq.inch
                return (int(q.rescale(pq.ft)), int(float((q.rescale(pq.ft) % pq.ft).rescale(pq.inch))), value)
            except TypeError:
                pass
        return (None, None, None)

    def render(self, name, value, attrs=None):
        if self.is_localized:
            for widget in self.widgets:
                widget.is_localized = self.is_localized
        # value is a list of values, each corresponding to a widget
        # in self.widgets.
        if not isinstance(value, list):
            value = self.decompress(value)
        output = []
        final_attrs = self.build_attrs(attrs)
        id_ = final_attrs.get('id', None)

        index = 0
        for i, widget in zip(['ft', 'in', 'cm'], self.widgets):
            try:
                widget_value = value[index]
            except IndexError:
                widget_value = None
            if id_:
                final_attrs = dict(final_attrs, id='%s_%s' % (id_, i))
            output.append(widget.render(name + '_%s' % i, widget_value, final_attrs))
            index += 1

        return render_to_string(self.template_name, {
            'id': id_,
            'name': name,
            'widget': mark_safe(self.format_output(output)),
            'module_name': str(self.form_class.__module__),
            'klass_name': self.form_class.__name__,
        })

    def format_output(self, rendered_widgets):
        return "%s ft %s in or %s cm" % (rendered_widgets[0], rendered_widgets[1], rendered_widgets[2])

    def value_from_datadict(self, data, files, name):
        return [w.value_from_datadict(data, files, name + '_%s' % i) for i, w in zip(['ft', 'in', 'cm'], self.widgets)]

    def value_omitted_from_data(self, data, files, name):
        for n in [name + '_%s' % i for i in ('ft', 'in', 'cm')]:
            if n not in data:
                return True
        return False


class LengthWidget(HeightWidget):
    template_name = 'unitology/length_field.html'


class LengthMultiWidget(HeightMultiWidget):
    template_name = 'unitology/length_multi_field.html'

    def __init__(self, units, attrs=None):
        widgets = (
            forms.Select(attrs=attrs, choices=[(v, str(v)) for v in range(0, 40)]),
            forms.Select(attrs=attrs, choices=[(v, str(v)) for v in range(0, 12)]),
            forms.TextInput(attrs=attrs),
        )
        super(HeightMultiWidget, self).__init__(units, widgets, attrs)


class SecondsWidget(BaseWidget):
    template_name = 'unitology/seconds_field.html'

    def __init__(self, units, *args, **kwargs):
        super(SecondsWidget, self).__init__(units, *args, **kwargs)

    def get_template_name(self, postfix=None):
        return self.template_name


class SecondsMultiWidget(BaseMultiWidget):
    template_name = 'unitology/seconds_ext_field.html'

    def __init__(self, units=None, attrs=None):
        widgets = (
            forms.TextInput(attrs={'maxlength': 2}),
            forms.TextInput(attrs={'maxlength': 2}),
        )
        super(SecondsMultiWidget, self).__init__(units, widgets, attrs)

    def decompress(self, value):
        if value:
            if isinstance(value, (list, tuple)):
                return tuple(value)
            return (str(int(value) // 60), str(int(value) % 60))
        return (None, None)

    def render(self, name, value, attrs=None):
        if self.is_localized:
            for widget in self.widgets:
                widget.is_localized = self.is_localized
        # value is a list of values, each corresponding to a widget
        # in self.widgets.
        if not isinstance(value, list):
            value = self.decompress(value)
        output = []
        final_attrs = self.build_attrs(attrs)
        id_ = final_attrs.get('id')
        for i, widget in enumerate(self.widgets):
            try:
                widget_value = value[i]
            except IndexError:
                widget_value = None
            if id_:
                final_attrs = dict(final_attrs, id='%s_%s' % (id_, i))
            output.append(widget.render(name + '_%s' % i, widget_value, final_attrs))
        return mark_safe(self.format_output(output))

    def format_output(self, rendered_widgets):
        return render_to_string(self.template_name, {
            'widget': rendered_widgets,
        })                                
