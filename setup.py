# coding: utf-8
import re
import os
from setuptools import setup


def read_file(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


def get_version():
    meta_filedata = read_file('src/yowsup-cli')
    return re.search(r'__version__ = "([^"]*)"', meta_filedata).group(1)


setup(
    name='Yowsup',
    version=get_version(),
    author='Tarek Galal',
    author_email='tare2.galal@gmail.com',
    description='Yowsup opened Whatsapp service under platforms!',
    license='MIT',
    url='https://github.com/tgalal/yowsup',
    package_dir={'': 'src'},
    long_description=read_file('README.md'),
    install_requires=['python-dateutil'],
)
