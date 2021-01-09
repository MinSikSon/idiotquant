# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='idiotquant',
    version='0.1.0',
    description='to get invest list',
    long_description=readme,
    author='Dokeun Oh, Minsik Son',
    author_email='ohdoking@gmail.com, tofu89223@gmail.com',
    url='https://github.com/MinSikSon/idiotquant',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
