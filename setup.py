# -*- coding: utf-8 -*-
from distutils.core import setup

with open('spectacles/requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='django-spectacles',
    version='0.0.3',
    author=u'Christo Crampton',
    packages=['spectacles'],
    include_package_data=True,
    install_requires=required,
    url='https://github.com/toast38coza/django-spectacles',
    license='MIT licence, see LICENCE',
    description='Tools for BDD built on top of django\'s ' + \
                ' unit testing framework',
    long_description=open('README.md').read(),
)
