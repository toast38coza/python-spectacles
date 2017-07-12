from setuptools import setup

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(name='python-spectacles',
      version='1.4.1',
      description='Description',
      author=u'Christo Crampton',
      license='MIT',
      packages=['spectacles'],
      install_requires=required,
      zip_safe=False)