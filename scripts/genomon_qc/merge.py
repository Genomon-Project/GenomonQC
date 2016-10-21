# -*- coding: utf-8 -*-
"""
Created on Thu Oct 20 13:27:27 2016

@author: okada
"""

def run(bamstats_file, coverage_file, output, meta):

    # read .bamstat
    f = open(bamstats_file)
    text = f.read()
    f.close()
    bamstat = text.split("\n")
    
    if len(bamstat) < 2:
        bamstat = ["",""]
        
    # read .coverage
    f = open(coverage_file)
    text = f.read()
    f.close()
    coverage = text.split("\n")
    
    if len(coverage) < 2:
        coverage = ["",""]
        
    f = open(output, "w")
    f.write(meta + "\n")
    f.write(bamstat[0] + "\t" + coverage[0] + "\n")    # header
    f.write(bamstat[1] + "\t" + coverage[1])    # data
    f.close()
