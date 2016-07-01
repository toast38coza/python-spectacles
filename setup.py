# -*- coding: utf-8 -*-
from distutils.core import setup

with open('spectacles/requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='python-spectacles',
    version='1.3.0',
    author=u'Christo Crampton',
    packages=['spectacles'],
    include_package_data=True,
    install_requires=required,
    entry_points='''
        [console_scripts]
        spectacles=spectacles.runner:run
    ''',
    url='https://github.com/toast38coza/python-spectacles',
    license='MIT licence, see LICENCE',
    description='Write e2e tests in yml. Run with Selenium. Report with Markdown',
    long_description=open('README.md').read(),
)
