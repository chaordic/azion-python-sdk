#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
from os import path

from setuptools import find_packages, setup

NAME = 'azion'
DESCRIPTION = "Azion Python SDK to interact with Azion REST API"
URL = 'https://github.com/raphapr/azion-sdk-python'
EMAIL = 'raphaelpr01@gmail.com'
AUTHOR = 'Raphael P. Ribeiro'
REQUIRES_PYTHON = '>=2.7.0'
VERSION = '0.0.1'
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
    license='MIT',
)
