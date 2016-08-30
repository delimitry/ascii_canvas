#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
Setup file, used to install or test 'asciicanvas'
"""

import os
from setuptools import setup


setup(
    name='asciicanvas',
    version='0.0.1',
    author='Dmitry Alimov',
    description='ASCII canvas for drawing in console using ASCII chars',
    license='MIT',
    keywords='ascii canvas console terminal',
    url='https://github.com/delimitry/ascii_canvas',
    packages=['asciicanvas'],
    test_suite='tests',
    zip_safe=False,
    classifiers=[
        'Environment :: Console',
        'Environment :: Win32 (MS Windows)',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'License :: OSI Approved :: MIT License',
        'Topic :: Multimedia :: Graphics',
    ],
)
