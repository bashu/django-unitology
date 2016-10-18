# -*- coding: utf-8 -*-

from django.http import HttpResponse

from .conf import settings


def reload(request, *args, **kwargs):
    try:
        field_class = getattr(
            __import__(
                request.GET.get('module_name'),
                fromlist=[request.GET.get('klass_name')],
            ),
            request.GET.get('klass_name'),
        )
    except:
        field_class = None

    if request.is_ajax() and field_class is not None:
        from_units = request.GET.get('from_units')
        to_units = request.GET.get('to_units')

        if 'value[]' in request.GET.keys():
            value = request.GET.getlist('value[]')
            for idx in range(0, len(value)):  # fix list of values...
                if not value[idx]:
                    value[idx] = str(0)
        else:
            value = request.GET.get('value', None)

        field = field_class(from_units, required=False)
        if value and from_units != to_units:
            value = field.conversion(value, from_units, to_units)
            if from_units != settings.UNITOLOGY_DATABASE_UNITS:
                field.widget.units = to_units

        html = field.widget.render(request.GET.get('name'), value, attrs={
            'id': request.GET.get('id'),
        })
        return HttpResponse(status=200, content=html, content_type='text/html')

    return HttpResponse(status=400)
