#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# """The setup script."""
#
from setuptools import setup, find_packages

setup(
        entry_points={
            'console_scripts': [
                'automation=qa_automation_drt_haw:main',
                ],
            },
        packages=find_packages(include=['qa_automation_drt_haw']),
        test_suite='tests'
        )
