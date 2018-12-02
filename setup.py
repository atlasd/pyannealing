#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import subprocess
import pip
import sys
import setuptools



setup(
    name='simulatedannealing',
    version='0.1',
    packages=find_packages(),
    package_dir={'simulatedannealing':'pyannealing'},
    include_package_data=True
)
