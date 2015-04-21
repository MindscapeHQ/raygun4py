import sys
from setuptools import setup

if sys.version_info[0] == 2:
    base_dir = 'python2'
elif sys.version_info[0] == 3:
    base_dir = 'python3'

setup(
    name='raygun4py',
    version='2.2.0',
    packages=['raygun4py', 'raygun4py.middleware'],
    package_dir= {
        "raygun4py": base_dir + "/raygun4py"
    },
    license='LICENSE',
    url='https://raygun.io',
    author='Raygun',
    author_email='hello@raygun.io',
    description='Official Raygun provider for Python 2.6/2.7 and Python 3+',
    long_description=open('README.rst').read(),
    install_requires=[
        'jsonpickle == 0.7.0',
        'blinker == 1.3.0'
    ],
    entry_points={
        'console_scripts': [
            'raygun4py = raygun4py.cli:main'
        ]
    },
    classifiers=[
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
