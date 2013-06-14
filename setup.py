import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README.md file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "GD Shortener",
    version = "0.0.1",
    author = "Gian Luca Dalla Torre",
    author_email = "gianluca@gestionaleauto.com",
    description = ("A module that provides access to .gd URL Shortener"),
    license = "LGPL",
    keywords = "url shortener gd",
    url = "https://github.com/torre76/gd_shortener",
    packages=['tests'],
    scripts=['gdshortener.py'],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
    ],
)