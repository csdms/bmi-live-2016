#! /usr/bin/env python
from ez_setup import use_setuptools
use_setuptools()
from setuptools import setup, find_packages


setup(name='bmi-live',
      version='0.1.0',
      author='CSDMS',
      author_email='csdms@colorado.edu',
      license='MIT',
      description='BMI Python example',
      long_description=open('README.md').read(),
      packages=find_packages(exclude=['*.tests']),
)
