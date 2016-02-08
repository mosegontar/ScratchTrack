#!/usr/bin/env python

from setuptools import setup

setup(
    name = 'scratchtrack',
    version = '1.0',
    author = 'Alex Gontar',
    url = 'https://github.com/mosegontar/ScratchTrack.git',
    description = 'Tag and track miscellaneous files in local directories',
    license = 'MIT',
    packages = ['scratchtrack'],
    install_requires = [peewee],
    entry_points = {
        'console_scripts': ['strack = scratchtrack.main:run']
    }

)