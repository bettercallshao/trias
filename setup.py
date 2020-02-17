# -*- coding: utf-8 -*-
"""Setup for trias."""

from setuptools import setup

_locals = {}
with open('trias/_version.py') as fp:
    exec(fp.read(), None, _locals) # noqa
version = _locals['version']

setup(
    name='trias',
    version=version,
    license='Apache',
    packages=['trias'],
)
