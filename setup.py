import re
from setuptools import setup

init_py = open('yowsup/__init__.py').read()
metadata = dict(re.findall("__([a-z]+)__ = ['|\"]([^']+)['|\"]", init_py))
metadata['doc'] = re.findall('"""(.+)"""', init_py)[0]

setup(
    name='yowsup',
    version=metadata['version'],
    description=metadata['doc'],
    author=metadata['author'],
    author_email=metadata['email'],
    url=metadata['url'],
    packages=['yowsup'],
    include_package_data=True,
    install_requires=[
        'python-dateutil < 2.3.0',
        'argparse < 1.3.0',
    ],
    entry_points={
        'console_scripts': [
            'yowsup = yowsup.cli:main',
        ],
    },
    license=open('MIT-LICENSE.txt').read(),
)
