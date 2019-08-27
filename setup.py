#!/usr/bin/env python3
"""Installer"""

from setuptools import find_packages, setup

with open('requirements.txt', 'rt') as reqs_file:
    REQUIREMENTS = reqs_file.readlines()

setup(
    name='python-template-flask',
    description='Flask project template.',
    long_description=open('README.md').read(),
    author='Sijis Aviles',
    author_email='email@example.com',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    setup_requires=['setuptools_scm'],
    use_scm_version={'local_scheme': 'dirty-tag'},
    install_requires=REQUIREMENTS,
    include_package_data=True,
    keywords='template flask',
    url='https://github.com/sijis/python-template-flask',
    download_url='https://github.com/sijis/python-template-flask',
    platforms=['OS Independent'],
    entry_points={},
)
