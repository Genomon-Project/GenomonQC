#!/usr/bin/env python

from distutils.core import setup

setup(name='genomon_qc',
      version='1.0.0',
      description='Python tools for running genomon QC for cancer genome and transcriptome sequencing analysis',
      author='Ai Okada',
      author_email='genomon_team@gamil.com',
      url='https://github.com/Genomon-Project/GenomonSummary.git',
      package_dir = {'': 'scripts'},
      packages=['genomon_qc', 'genomon_qc.resource', 'genomon_qc.config'],
      scripts=['genomon_qc'],
      license='GPL-3'
     )
