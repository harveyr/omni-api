#!/usr/bin/env python

import os
from setuptools import setup, find_packages
from pip.req import parse_requirements

install_requires = parse_requirements(
    os.path.join(
        os.path.split(os.path.realpath(__file__))[0],
        'requirements.txt'
    )
)

setup(
    name='omni-api',
    version='0.1',
    description='API stuffs',
    author='Harvey Rogers',
    author_email='harveyr@gmail.com',
    packages=find_packages(),
    install_requires=[str(ir.req) for ir in install_requires]
)
