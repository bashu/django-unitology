django-unitology
================

Custom model fields to store, retrieve and convert measurements of height, weight and more.

Authored by `Basil Shubin <https://github.com/bashu>`_,  and some great
`contributors <https://github.com/bashu/django-unitology/contributors>`_.

.. image:: https://img.shields.io/pypi/v/django-unitology.svg
    :target: https://pypi.python.org/pypi/django-unitology/

.. image:: https://img.shields.io/pypi/dm/django-unitology.svg
    :target: https://pypi.python.org/pypi/django-unitology/

.. image:: https://img.shields.io/github/license/bashu/django-unitology.svg
    :target: https://pypi.python.org/pypi/django-unitology/

.. image:: https://img.shields.io/travis/bashu/django-unitology.svg
    :target: https://travis-ci.org/bashu/django-unitology/

Installation
------------

.. code-block:: bash

    pip install django-unitology

External dependencies
~~~~~~~~~~~~~~~~~~~~~

* jQuery - this is not included in the package since it is expected
  that in most scenarios this would already be available.

Setup
-----

Add ``unitology`` to  ``INSTALLED_APPS``:

.. code-block:: python

    INSTALLED_APPS += (
        'unitology',
    )

Update your ``urls.py`` file:

.. code-block:: python

    urlpatterns += [
        url(r'^unitology/', include('unitology.urls')),
    ]

When deploying on production server, don't forget to run:

.. code-block:: shell

    python manage.py collectstatic

Usage
-----

.. code-block:: python

    # models.py

    from django.db import models
    from django.contrib import admin

    from unitology.models import UnitsFieldMixin
    from unitology.fields import WeightField, HeightField
    from unitology.forms import UnitsFieldFormMixin


    class Person(UnitsFieldMixin):

        name = models.CharField(max_length=128)

        weight = WeightField(blank=True, null=True)
        height = HeightField(blank=True, null=True)


    class PersonChangeForm(UnitsFieldFormMixin):

        class Meta:
            model = Person


    class PersonAdmin(admin.ModelAdmin):
        form = PersonChangeForm


    admin.site.register(Person, PersonAdmin)

Please see ``example`` application. This application is used to manually test the functionalities of this package. This also serves as a good example.

You need only Django 1.4 or above to run that. It might run on older versions but that is not tested.


License
-------

``django-unitology`` is released under the MIT license.
