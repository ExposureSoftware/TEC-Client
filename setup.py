import sys
from setuptools import find_packages
from pkg_resources import resource_filename
from cx_Freeze import setup, Executable

__author__ = 'ToothlessRebel'

build_exe_options = {
    "include_files": [
        ('resources', 'resources'),
        ('config.ini', 'config.ini'),
        'plugins'
    ]
}

base = None

setup(
    name="Centurion Client",
    version="0.5.3-alpha",
    description="TEC Client in Python",
    options={
        "build_exe": build_exe_options
    },
    packages=find_packages(),
    package_data={'': ['*.png', '*.gif', '*.ico']},
    executables=[
        Executable(
            "main.py",
            base=base,
            icon=resource_filename('resources.images', 'centurion.ico'),
            targetName="Centurion Client.exe",
            packages=find_packages()
        )
    ]
)