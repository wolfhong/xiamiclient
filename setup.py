#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name="xiamiclient",
    version="0.10",
    license="MIT",
    description="xiami-music service: search/detail/download",
    author="wolfhong",
    author_email="hongxucai1991@163.com",
    packages=find_packages(),
    zip_safe=False,
    platforms='any',
    install_requires=[
        'requests>=2.2.1',
    ],
)
