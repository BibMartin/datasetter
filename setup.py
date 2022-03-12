from setuptools import setup, find_packages

setup(
    name='datasetter',
    version='0.0.0',
    description='Create & share your datasets with python.',
    author='Martin Journois',
    url='https://github.com/BibMartin/datasetter',
    packages=find_packages(include=['datasetter', 'datasetter.*']),
    install_requires=[],
    setup_requires=['pytest-runner', 'flake8'],
    tests_require=['pytest'],
    )
