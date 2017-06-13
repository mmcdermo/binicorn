#!/usr/bin/env python
from setuptools import setup, find_packages

install_requires = [
    'numpy'
]

setup(
    name='binicorn',
    version='0.1',
    description='Binicorn file format for numpy data with unstructured metadata',
    author='Morgan McDermott',
    author_email='morganmcdermott@gmail.com',
    long_description='',
    url='https://github.com/mmcdermo/binicorn',
    license='All rights reserved',
    zip_safe=False,
    keywords='',
    packages=find_packages(),
    install_requires=install_requires,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
    ]
)
