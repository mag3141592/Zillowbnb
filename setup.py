"""
Setup module for ZillowBnb
ZillowBnb is not pip installable
"""

from setuptools import setup, find_packages

AUTHOR = 'ablew, hmurph3, mag3141592, rileywaters'
DESCRIPTION = 'Zestimate for AirBnb Listings'
LICENSE = open('LICENSE').read()
LONG_DESCRIPTION_CONTENT_TYPE = 'text/markdown'
NAME = 'ZillowBnb'
PACKAGES = find_packages()
URL = 'https://github.com/mag3141592/Zillowbnb'

# reads in the README.md
with open('README.md', 'r') as file:
    LONG_DESCRIPTION = file.read()

OPTS = dict(name=NAME,
            description=DESCRIPTION,
            long_description=LONG_DESCRIPTION,
            long_description_content_type=LONG_DESCRIPTION_CONTENT_TYPE,
            url=URL,
            license=LICENSE,
            author=AUTHOR,
            packages=PACKAGES)

if __name__ == '__main__':
    setup(**OPTS)
