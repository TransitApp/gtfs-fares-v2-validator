from setuptools import setup

setup(
    name='gtfs-fares-v2-validator',
    version='1.0.0',
    description=
    'Validate transit feeds for conformance to the GTFS Fares v2 specification',
    url='https://github.com/TransitApp/gtfs-fares-v2-validator',
    author='Jeremy Steele',
    packages=['fares_validator'],
    classifiers=['License :: OSI Approved :: MIT License'],
    zip_safe=False,
    install_requires=[])
