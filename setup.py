from setuptools import setup

setup(
    name='raygun4py',
    version='1.1.3',
    packages=['raygun4py'],
    license='LICENSE',
    url='http://raygun.io',
    author='Mindscape',
    author_email='contact@mindscape.co.nz',
    long_description=open('README.rst').read(),
    install_requires=[
        "jsonpickle == 0.7.0"
    ],
)
