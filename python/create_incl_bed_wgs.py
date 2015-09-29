# -*- coding: utf-8 -*-
"""
Created on Thu Sep 17 09:37:53 2015

@author: okada
"""

import argparse
import os
import math

#import sys
#sys.argv=[".", "-i", "C:/cygwin64/home/okada/install/bedtools2-master/genomes/human.hg19.genome", "-o", "./test.bed", "-w", "1000000"]

#
# Main
#
def main():

#
# Argument parse
#
    parser = argparse.ArgumentParser( description = "create BED file, use `bedtools shuffle -incl` for WGS." )
    parser.add_argument( '-i', '--input_genome', help = "Input genome file", type = str )
    parser.add_argument( '-o', '--output_bed', help = "Output bed file", type = str )
    parser.add_argument( '-w', '--width', help = "Bases per one line", type = long )
    parser.add_argument( '-c', '--chr', help = "'chr' or None", type = str, default = None )
    
    # arg parse
    arg = parser.parse_args()
    
    if not os.path.exists(arg.input_genome):
        print "Not exist file, " + arg.input_genome
        return

    # read genome file to dict.
    f = open(arg.input_genome, "r")
    genomes = {}    
    for line in f:
        cells = line.split("\t")
        if len(cells) < 2:
            break
        genomes.update({cells[0]:long(cells[1].rstrip('rn'))})

    f.close()
    
    # write BED file
    f = open(arg.output_bed, "w") 
    for i in range(24):
        if i == 22:
            title = "chrX"
        elif i == 23:
            title = "chrY"        
        else:
            title = "chr" + str(i+1)
        
        size = genomes[title]
        start = 0
        end = arg.width
        
        line_num = long(math.ceil(float(size)/float(arg.width)))
        for j in range(line_num):
            if end > size:
                end = size
            
            if i == 22:
                head = arg.chr + "X"
            elif i == 23:
                head = arg.chr + "Y"
            else:
                head = arg.chr + str(i+1)

            f.write("{0}\t{1}\t{2}\n".format(head, start, end))
            start = end
            end += arg.width

    f.close()
    
if __name__ == "__main__":
    main()


