import sys
from setuptools import setup

packages = ['raygun4py', 'raygun4py.middleware']

base_dir = 'python2'
if sys.version_info[0] == 3:
    base_dir = 'python3'

exec(open('%s/raygun4py/version.py' % base_dir).read())
requirements = [
    'jsonpickle >= 0.9.2',
    'blinker >= 1.3.0',
    'requests >= 2.9.1'
]

dev_requirements = [
    'unittest2 >= 1.1.0',
    'coveralls >= 1.5.1',
    'mock >= 2.0.0',
    'django == 1.8.8',
    'flask >= 0.10',
    'WebTest >= 2.0.32'
]

setup(
    name='raygun4py',
    version=__version__,
    packages=packages,
    package_dir= {
        "raygun4py": base_dir + "/raygun4py"
    },
    license='LICENSE',
    url='https://raygun.com',
    author='Raygun',
    author_email='hello@raygun.io',
    description='Official Raygun provider for Python 2.7 and Python 3+',
    long_description=open('README.rst').read(),
    install_requires=requirements,
    extras_require={
        'dev': dev_requirements
    },
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
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Communications',
    ],
)
