"""
This file exists to contain all Django and Python compatibility issues.

In order to avoid circular references, nothing should be imported from
unitology.

"""

import sys
import django

try:
    from django.utils.functional import curry
except ImportError:
    from functools import partial as curry

if django.VERSION[:2] < (1, 5):
    # If the user is using Django < 1.5, then load up the url tag
    # from future. Otherwise use the normal one. The purpose of this
    # is to get the url template tag that supports context variables
    # for the first argument, yet won't raise a deprecation warning
    # about importing it from future.
    from django.templatetags.future import url  # NOQA
else:
    from django.template.defaulttags import url  # NOQA
