import sys
from setuptools import setup

if sys.version_info[0] == 2:
    base_dir = 'python2'
elif sys.version_info[0] == 3:
    base_dir = 'python3'

setup(
    name='raygun4py',
    version='2.0.0',
    packages=['raygun4py'],
    package_dir= {
        "raygun4py": base_dir + "/raygun4py"
    },
    license='LICENSE',
    url='http://raygun.io',
    author='Mindscape',
    author_email='contact@mindscape.co.nz',
    long_description=open('README.rst').read(),
    install_requires=[
        "jsonpickle == 0.7.0"
    ],
)
