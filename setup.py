from setuptools import setup

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(name='python-spectacles',
      version='1.4.2',
      description='Description',
      author=u'Christo Crampton',
      license='MIT',
      packages=['spectacles'],
      install_requires=[
          'splinter==0.7.5',
          'requests==2.10.0',
          'PyYAML==3.11',
          'click==6.6'
      ],
      zip_safe=False)