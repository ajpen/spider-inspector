#!/usr/bin/env python
# -*- coding: utf-8 -*-


import io
import os

from setuptools import find_packages, setup

# Package meta-data.
NAME = 'scrapy_inspector'
DESCRIPTION = 'Real time scrapy request inspection'
# URL = 'https://github.com/me/myproject'
# EMAIL = 'me@example.com'
AUTHOR = 'Anfernee Jervis'

REQUIRED = [
    'autobahn',
    'twisted',
    'scrapy'
]


here = os.path.abspath(os.path.dirname(__file__))

with io.open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = '\n' + f.read()


setup(
    name=NAME,
    version='0.1.0',
    description=DESCRIPTION,
    long_description=long_description,
    author=AUTHOR,
    # author_email=EMAIL,
    # url=URL,
    packages=find_packages(exclude=('tests',)),
    install_requires=REQUIRED,
    include_package_data=True,
    license='MIT',
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ]
)
