#!/usr/bin/env python
# 
# $Id: setup.cfg 134 2016-03-30 09:28:00Z aokada $
# 

from setuptools import setup, find_packages

version = '1.1.0'

setup(name='genomon_qc',
      version=version,
      description="parser result files created by genomon",
      long_description="""\n
Genomon Quality Control""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='genomon quality-control',
      author='aokada',
      author_email='genomon_team@gamil.com',
      url='https://github.com/Genomon-Project/GenomonQC.git',
      license='GPL-3',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      scripts=['genomon_qc'],
      data_files=[('config', ['genomon.cfg'])],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )

