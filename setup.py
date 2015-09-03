#!/usr/bin/env python

import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as f:
        readme = f.read()

setup(
    name='clifactory',
    version='0.1.0',
    description='Command line made as easy as a web app',
    long_description=readme,
    author='Thomas Maurice',
    author_email='thomas@maurice.fr',
    license='GPLv3',
    url='https://github.com/thomas-maurice/clifactory',
    packages=['clifactory'],
    platforms='any',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 2.7',
    ],
    
    license="WTFPL",
)
