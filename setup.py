#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name = 'scratchtrack'
    version = '1.0'
    author = 'Alex Gontar'
    url = 'https://github.com/mosegontar/ScratchTrack.git'
    description = 'Tag and track miscellaneous files in local directories'
    license = 'MIT'
    packages = find_packages()
    install_requires = []
    entry_points = {
        'console_scripts': ['strack = scratchtrack.main:run]
    }

)