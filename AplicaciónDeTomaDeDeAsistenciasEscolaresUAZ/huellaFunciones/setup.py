# -*- coding: utf-8 -*-

import os
from distutils.core import setup, Extension

setup(
    name="pyfprint-cffi",
    version="0.1",
    license="GPL-2",
    packages=["pyfprint"],
    install_requires=[
        "cffi==0.8.6",
        "Pillow",
    ],
)
