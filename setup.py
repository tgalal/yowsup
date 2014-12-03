from __future__ import print_function
from setuptools import setup, find_packages
import yowsup
import platform

deps = ['python-dateutil', 'argparse']

if platform.system().lower() == "windows":
    deps.append('pyreadline')
else:
    deps.append('readline')

setup(
    name='yowsup',
    version=yowsup.__version__,
    url='http://github.com/tgalal/yowsup/',
    license='MIT License',
    author='Tarek Galal',
    tests_require=[],
    install_requires = deps,
    scripts = ['yowsup-cli'],
    #cmdclass={'test': PyTest},
    author_email='tare2.galal@gmail.com',
    description='A WhatsApp python library',
    #long_description=long_description,
    packages= find_packages(),
    include_package_data=True,
    platforms='any',
    #test_suite='',
    classifiers = [
        'Programming Language :: Python',
        'Development Status :: 4 - Beta',
        'Natural Language :: English',
        #'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules'
        ],
    #extras_require={
    #    'testing': ['pytest'],
    #}
)