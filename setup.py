#!/usr/bin/env python

from setuptools import setup

setup(name='gomon',
      version='0.1',
      description='Go CD Build Monitor',
      author='Moritz Lenz',
      author_email='moritz.lenz@gmail.com',
      packages=['gomon'],
      package_data={'gomon': ['static/*', 'templates/*.html']},
      requires=['flask', 'gunicorn', 'gocd', 'humanize'],
     )
