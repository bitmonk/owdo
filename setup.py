from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='owdo',
      version=version,
      description="opsworks do",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='aws opsworks boto',
      author='Justin Alan Ryan',
      author_email='bitmonk@icloud.com',
      url='',
      license='AGPL2',
      package_dir = {'': 'src'},
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=True,
      install_requires=[
        'cement',
        'boto',
      ],
      entry_points={
        'console_scripts': ['owdo=owdo.command_line:main'],
      },
      )
