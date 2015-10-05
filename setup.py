#!/usr/bin/env python

from distutils.core import setup

setup(name='genomon_summary',
      version='0.1.0',
      description='Python tools for running genomon summary for cancer genome and transcriptome sequencing analysis',
      author='Ai Okada',
      author_email='genomon_team@gamil.com',
      url='https://github.com/Genomon-Project/Genomon.git',
      package_dir = {'': 'scripts'},
      packages=['genomon_summary', 'genomon_summary.resource', 'genomon_summary.config'],
      scripts=['genomon_summary'],
      license='GPL-3'
     )
