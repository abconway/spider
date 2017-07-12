from setuptools import setup, find_packages
import os
import sys

__version__ = '0.0.1'
__requirements__ = [
    'boto3==1.4.4',
    'click==6.7',
    'PyYAML==3.12',
]

setup(
    name='spider',
    version=__version__,
    packages=find_packages(),
    include_package_data=True,
    install_requires=__requirements__,
    entry_points='''
    [console_scripts]
    spider=spider.scripts.cli:cli
    ''',
)
