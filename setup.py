#!/usr/bin/env python

import os
import re
import sys
import codecs

from setuptools import setup, find_packages

def read(*parts):
    file_path = os.path.join(os.path.dirname(__file__), *parts)
    return codecs.open(file_path, encoding='utf-8').read()


def find_version(*parts):
    version_file = read(*parts)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return str(version_match.group(1))
    raise RuntimeError("Unable to find version string.")


setup(
    name='django-unitology',
    version=find_version('unitology', '__init__.py'),
    license='MIT License',

    install_requires=[
        'quantities',
        'numpy',
    ],
    requires=[
        'Django (>=1.4.2)',
    ],

    description="Height / Weight fields for Django models & forms with unit conversion",
    long_description=read('README.rst'),

    author='Basil Shubin',
    author_email='basil.shubin@gmail.com',

    url='https://github.com/bashu/django-unitology',
    download_url='https://github.com/bashu/django-unitology/zipball/master',

    packages=find_packages(exclude=('example*', '*.tests*')),
    include_package_data=True,

    tests_require=[
        'django-setuptest',
        'django-dynamic-fixture',
    ],
    test_suite='setuptest.setuptest.SetupTestSuite',

    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
