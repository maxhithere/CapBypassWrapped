from setuptools import setup, find_packages

setup(
    name='capbypasswrapped',
    version='1.1',
    packages=find_packages(),
    setup_requires=['setuptools_scm', 'wheel'],
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=[
        'requests',
        'logging'
    ],
)
