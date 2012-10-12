#!/usr/bin/env python

from setuptools import setup, find_packages

CLASSIFIERS = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Natural Language :: English',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Topic :: Eve Online'
]

setup(name='django-eve-igb',
    version='1.0',
    description='Classes and functions that help handling the Eve Online ingame Browser (IGB) in Django.',
    author='Jens Lauterbach',
    author_email='lauterjens@googlemail.com',
    url='https://github.com/jenslauterbac/django-eve-igb',
    packages=['eveigb'],
    install_requires=['django'],
    tests_require=[
        'django-nose',
        'coverage',
        'django-coverage'
    ],
    test_suite='eveigb.tests.runtests.runtests',
    provides=['eveigb'],
    classifiers=CLASSIFIERS
)