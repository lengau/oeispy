from setuptools import setup, find_packages

setup(
    name='oeispy',
    version='0.0.1',
    packages=find_packages(exclude=['tests']),
    requires=['requests'],
    tests_require=['pytest']
)
