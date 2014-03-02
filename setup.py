# -*- coding: utf-8 -*-
from distutils.core import setup

setup(
    name='django-spectacles',
    version='0.0.1',
    author=u'Christo Crampton',
    packages=['spectacles'],
    include_package_data=True,
    url='https://github.com/toast38coza/django-spectacles',
    license='MIT licence, see LICENCE',
    description='Tools for BDD built on top of django\'s ' + \
                ' Institute to GeoDjango',
    long_description=open('README.md').read(),
    zip_safe=False,
)
