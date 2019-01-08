#/usr/bin/env python3

from setuptools import setup, find_packages

setup(
    name='mongo-backup-cli',
    version='0.1.0',
    author='Jonas A. Walther',
    author_email='jonas@rehtlaw.me',
    packages=find_packages(),
    entry_points='''
    [console_scripts]
    mongo-backup=mongo_backup.cli:main
'''
)
