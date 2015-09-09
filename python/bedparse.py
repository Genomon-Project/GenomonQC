#! /usr/bin/python
"""

This is a Python parser module for annotation database


"""
import random
import os
################################################################################
#
# Bed file parser
#
################################################################################
class BedExtract:

    def __init__( self, input_bed, bin_size):
        self.data = []

        if input_bed != None:
            if os.path.exists(input_bed):
                file = open( input_bed, 'r' )
                result = self.parse_file( file )
                file.close()

            self.bin_size = 0
        else:
            self.bin_size = bin_size

        if False == result:
            print "Error parse database file"

    def parse_file( self, file ):

        try:
            for line in file:
                line_split = line.split()
                self.data.append(line_split)
    
            return True
            
        except Exception as e:
            print e
            return False
            
    def get_random_interval( self ):

        return_value = None
        pos = random.randrange( 0, len(self.data)-1 )

        if self.bin_size == 0:   
            return_value = self.data[pos]

        return return_value

    def save_random_bed( self, output_bed, sample_num ):

        try:        
            f = open(output_bed, "w")
            for i in range(sample_num):
                pos = random.randrange( 0, len(self.data)-1 )
                f.write("{0}\t{1}\t{2}\n".format(self.data[pos][0], self.data[pos][1], self.data[pos][2]))
    
            f.close()
            return True

        except Exception as e:
            print e
            return False
            
