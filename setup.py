#!/usr/bin/env python
from setuptools import setup, find_packages

__doc__="""
Falsify data
"""

version = '0.0.1'

setup(name='perjury',
    version=version,
    description=__doc__,
    author='Aaron Merriam',
    author_email='aaronmerriam@gmail.com',
    keywords='content',
    long_description=__doc__,
    url='https://github.com/aaronmerriam/foundry',
    packages=find_packages(),
    platforms="any",
    license='BSD',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Natural Language :: English',
    ],
)
