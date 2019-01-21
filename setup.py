#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
from os import path

from setuptools import find_packages, setup

NAME = 'azion-sdk'
DESCRIPTION = "A Python SDK to provides a pure interface for the Azion REST API v2"
URL = 'https://github.com/chaordic/azion-python-sdk'
EMAIL = 'raphaelpr01@gmail.com'
AUTHOR = 'Raphael P. Ribeiro'
REQUIRES_PYTHON = '>=2.7.0'
VERSION = '0.0.2'
REQUIRED = [
    'pendulum',
    'requests'
]


setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    install_requires=REQUIRED,
    include_package_data=True,
    license='GPL3',
)
