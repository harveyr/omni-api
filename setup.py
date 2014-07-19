#!/usr/bin/env python

from setuptools import setup, find_packages


setup(
    name='omni-api',
    version='0.1',
    description='API stuffs',
    author='Harvey Rogers',
    author_email='harveyr@gmail.com',
    packages=find_packages(),
    install_requires=[
        'requests >= 2.3.0',
        'requests_oauthlib >= 0.4.1',
        'python-dateutil >= 2.2',
    ]
)
