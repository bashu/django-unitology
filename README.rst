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

When deploying on production server, don't forget to run:

.. code-block:: shell

    python manage.py collectstatic

Usage
-----

License
-------

``django-unitology`` is released under the MIT license.
