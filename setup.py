# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='Log Abstractor',
    version='0.1.0',
    description='Log Abstractor For HDFS',
    long_description=readme,
    author='Wen ZQ',
    author_email='wen.zq@qq.com',
    url='https://github.com/nee541/log_abstract',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)

