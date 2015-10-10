__author__ = 'ToothlessRebel'
import sys
from setuptools import find_packages
from pkg_resources import resource_filename
from cx_Freeze import setup, Executable

build_exe_options = {
    "include_files": [
        ('resources', 'resources'),
        ('config.ini', 'config.ini')
    ]
}

base = None
# if sys.platform == "win32":
#     base = "Win32GUI"

setup(
    name="TEC Client",
    version="0.5.2-alpha",
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
            icon=resource_filename('resources.images', 'eternal_logo.ico'),
            targetName="TEC Client.exe",
            packages=find_packages()
        )
    ]
)