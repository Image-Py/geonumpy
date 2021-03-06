#!/usr/bin/env python3


from setuptools import setup
from setuptools import find_packages
import setuptools

setup(
    name="geonumpy",
    version="0.09",
    author="YXDragon",
    author_email="yxdragon@imagepy.org",
    license = "BSD 3-Clause",
    url = "http://imagepy.org/",
    description = "combine geo crs and mat with numpy array",
    install_requires = [
        "scikit-image",
        "numpy",
        "scipy",
        "matplotlib",
        "pandas",
        "geopandas",
    ],
    packages=setuptools.find_packages(),
)
