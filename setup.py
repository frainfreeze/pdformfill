from setuptools import setup, find_packages

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="pdformfill",
    version="0.0.3",
    author="Tomislav Kucar",
    author_email="kucar.tomislav@gmail.com",
    url="http://github.com/frainfreeze/pdformfill",
    description="library for filling pdf forms",
    long_description=long_description,
    long_description_content_type='text/markdown',
    scripts = [],
    license = "BSD-3-Clause",
    platforms = ["any"],
    zip_safe=False,
    packages=find_packages()
    )
    
