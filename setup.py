#!/usr/bin/env python
# coding=utf-8

from setuptools import find_packages, setup
from kmap import VERSION


setup(
    name='AWD_Tools',
    version=VERSION,
    url='git@github.com:Ro0tk1t/awd_tools.git',
    description='AWD scanner',
    author='ro0tk1t',
    packages=find_packages(),
    python_requires=">=3.7",
    include_package_data=True,
    entry_points={
        "console_scripts":[
            'tony = awd_tools.scanner.Marvel:main',
        ]
    },

    install_requires=[
        'flask',
        'Flask-Admin',
        'Flask-Login',
        'Flask-MongoEngine',
        'Flask-Bootstrap',

        'yarl',
        'pymongo',
        'paramiko',
        'nest_asyncio',
        'async_timeout',
    ],
    extras_require={
        'build': [
            'devpi',
            'wheel',
        ]
    }
)
