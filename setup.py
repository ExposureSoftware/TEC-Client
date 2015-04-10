__author__ = 'ToothlessRebel'
from setuptools import setup, find_packages

setup(
    name='client',
    version='0.1',
    packages=find_packages(),
    package_data={'': ['*.png', '*.gif', '*.ico']}
)