from distutils.core import setup

setup(
    name='Raygun4py',
    version='0.1',
    packages=['provider',],
    license='LICENSE',
    long_description=open('README.rst').read(),
    install_requires=[
        "jsonpickle == 0.4.0"
    ],
)
