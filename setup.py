#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click>=6.0', 'upackage>=0.1.6']

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest', 'mock']

setup(
    author="Leonid Umanskiy",
    author_email='leonid.umanskiy@aofl.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="uGet Command Line Interface",
    entry_points={
        'console_scripts': [
            'uget=ugetcli.__main__:main',
        ],
    },
    install_requires=requirements,
    license="MIT",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='ugetcli',
    name='ugetcli',
    packages=find_packages(include=['ugetcli']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/AgeOfLearning/ugetcli',
    version='0.3.8',
    zip_safe=False,
)
