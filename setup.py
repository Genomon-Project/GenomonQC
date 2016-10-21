#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on Thu Oct 20 17:59:54 2016

@author: okada
"""

from setuptools import setup
from scripts.genomon_qc import __version__

setup(name='genomon_qc',
      version=__version__,
      description="Python tools for bam's Quality Control.",
      author='ai okada',
      author_email='genomon.devel@gmail.com',
      url='https://github.com/Genomon-Project/GenomonQC',
      package_dir = {'': 'scripts'},
      packages=['genomon_qc'],
      scripts=['genomon_qc'],
      license='License of GenomonPipeline'
      )
