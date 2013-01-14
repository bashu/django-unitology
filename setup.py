# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

version = '0.0.1'

setup(name='django-unitology',
      version=version,
      keywords='django weight height conversion',
      url='https://github.com/bashu/django-unitology',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      )
