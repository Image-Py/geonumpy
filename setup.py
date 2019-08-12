#!/usr/bin/env python3


from setuptools import setup
from setuptools import find_packages
import setuptools


setup(
    name="geonumpy",
    version="0.1",
    author="YXDragon",
    author_email="yxdragon@imagepy.org",
    license = "BSD 3-Clause",
    url = "http://imagepy.org/",
    description = "This is an treat gis data with numpy Package.",
    install_requires = [
        "scikit-image",
        "numpy",
        "scipy",
        "matplotlib",
        "pandas",
        "geopandas",
        # "gdal",
        # "fiona",
        # "shapely",
    ],
    packages=setuptools.find_packages(),
)
