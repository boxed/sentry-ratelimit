#!/usr/bin/env python
# coding=utf-8
"""
sentry-ratelimit
==============

Plugin to sentry for rate limiting low volume errors you don't care about.

:license: BSD, see LICENSE for more details.
"""
from setuptools import setup, find_packages


install_requires = [
    'sentry>=8.15.0',
]

setup(
    name='sentry-ratelimit',
    version='0.2.0',
    author='Anders Hovmöller',
    author_email='boxed@killingar.net',
    url='http://github.com/boxed/sentry-ratelimit',
    description="Plugin to sentry for rate limiting low volume errors you don't care about",
    long_description=__doc__,
    license='BSD',
    packages=find_packages(exclude=['tests']),
    zip_safe=False,
    install_requires=install_requires,
    entry_points={
       'sentry.plugins': [
            'ratelimit = sentry_ratelimit.plugin:ratelimitMessage'
        ],
    },
    include_package_data=True,
    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Topic :: Software Development'
    ],
)
