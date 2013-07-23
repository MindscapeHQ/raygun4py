from distutils.core import setup

setup(
    name='raygun4py',
    version='1.0.0',
    packages=['raygun4py',],
    license='LICENSE',
    url='http://raygun.io',
    author='Mindscape',
    author_email='contact@mindscape.co.nz',
    long_description=open('README.rst').read(),
    install_requires=[
        "jsonpickle == 0.4.0"       
    ],
)
