# -*- coding: utf-8 -*-

import quantities as pq

from unitology import variables as units


def kg2lb(value):
    q = float(value) * pq.kg  # rescale kgs to lbs
    return float(q.rescale(pq.lb))


def lb2kg(value):
    q = float(value) * pq.lb  # rescale lbs to kgs
    return float(q.rescale(pq.kg))


def cm2in(value):
    q = float(value) * pq.cm  # rescale cms to inches
    return float(q.rescale(pq.inch))


def in2cm(value):
    q = float(value) * pq.inch  # rescale inches to cms
    return float(q.rescale(pq.cm))


def convert_weight(value, from_units, to_units):
    if from_units != to_units:
        if to_units == units.IMPERIAL:
            value = kg2lb(value)
        elif to_units == units.METRIC:
            value = lb2kg(value)
    return float(value)


def convert_length(value, from_units, to_units):
    if from_units != to_units:
        if to_units == units.IMPERIAL:
            value = cm2in(value)
        elif to_units == units.METRIC:
            value = in2cm(value)
    return float(value)
