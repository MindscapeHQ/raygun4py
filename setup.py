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
    ],classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Communications',
    ],
)
