#! /usr/bin/env python

from genomon_summary.stage_task import *

import xlwt
import re
   
class Res_Merge(Stage_task):
#class Res_Merge():
    task_name = "merge"

    script_template = """
#!/bin/bash
#
# Set SGE
#
#$ -S /bin/bash         # set shell in UGE
#$ -cwd                 # execute at the submitted dir
#$ -e {log}             # log file directory
#$ -o {log}             # log file directory
pwd                     # print current working directory
hostname                # print hostname
date                    # print date
set -xv

# cat {input1} {input2} {input3} {input4} > {output}
"""

    def __init__(self, qsub_option, script_dir):
        super(Res_Merge, self).__init__(qsub_option, script_dir)
#    def __init__(self):
#        pass
    
    def ToExcelString(self, i):

        j = 0
        alphabet_num = ord( 'Z' ) - ord( 'A' ) + 1
        while i > alphabet_num:
            j += 1
            i -= alphabet_num
    
        if j == 0:
            return_char = chr( ord( 'A' ) + i  - 1)
        else:
            return_char = chr( ord( 'A' ) + j - 1 ) + chr( ord( 'A' ) + i - 1)
    
        return return_char
    
    def mkxls(self, string, excel_file):

        number_target = re.compile( '^([0-9]+) \+ ([0-9]+) .+$' )
        ratio_target = re.compile( ' \(([0-9]+\.[0-9]+)%:' )
        f_type = None
        id = 0
        tsv_header = []
        tsv_values = []
        bam_stats_header = None
        bam_stats = []
        bam_stats_num = 0
    
        input_file = string.split("\n")
        for line in input_file:
            line = line.replace( "\n", "" )
            line_split = line.split( "\t" )
    
            # No.1 bamstat
            if line_split[ 0 ] == 'bam_filename':
                f_type = 'bam_stat'
                tsv_header += line_split
                bam_stats_header = line_split
    
            elif f_type == 'bam_stat' and line_split[ 0 ] != 'LIBRARY':
                if tsv_values == []:
                    tsv_values += line_split
                    id = len( line_split )
    
                bam_stats.append( line_split )
    
            # No.3 grep -A1 LIBRARY
            elif line_split[ 0 ] == 'LIBRARY':
                f_type = 'metrics'
                tsv_header += line_split
    
            elif f_type == 'metrics':
                tsv_values +=line_split
                f_type = ''
                
            # No.4 samtools flagstat
            elif line_split[ 0 ] == 'samtools_flagstat':
                f_type = 'flagstat'
    
            elif f_type == 'flagstat' and line_split[ 0 ] != 'non-N_total_depth':
                match_ratio = None
                type_string = None
                if -1 != line_split[ 0 ].find( 'in total (QC-passed reads + QC-failed reads)' ):
                    type_string = 'total'
                elif -1 != line_split[ 0 ].find( 'secondary' ):
                    type_string = 'secondary'
                elif -1 != line_split[ 0 ].find( 'supplementary' ):
                    type_string = 'supplementary'
                elif -1 != line_split[ 0 ].find( 'duplicates' ):
                    type_string = 'duplicates'
                elif -1 != line_split[ 0 ].find( 'mapped' ):
                    type_string = 'mapped'
                    match_ratio = ratio_target.search( line )
                elif -1 != line_split[ 0 ].find( 'paired in sequencing' ):
                    type_string = 'paired'
                elif -1 != line_split[ 0 ].find( 'read1' ):
                    type_string = 'read1'
                elif -1 != line_split[ 0 ].find( 'read2' ):
                    type_string = 'read2'
                elif -1 != line_split[ 0 ].find( 'properly paired' ):
                    type_string = 'properly_paired'
                    match_ratio = ratio_target.search( line )
                elif -1 != line_split[ 0 ].find( 'with itself and mate mapped' ):
                    type_string = 'with_itself_and_mate_mapped'
                elif -1 != line_split[ 0 ].find( 'singletons' ):
                    type_string = 'singletons'
                    match_ratio = ratio_target.search( line )
                elif -1 != line_split[ 0 ].find( 'with mate mapped to a different chr' ):
                    type_string = 'mate_mapped_to_a_diff_chr'
                elif -1 != line_split[ 0 ].find( 'with mate mapped to a different chr (mapq>=5)' ):
                    type_string = 'mate_mapped_to_a_diff_chr_mapq_5'
    
                if type_string:
                    tsv_header.append( 'flagstat_{type}_QC-passed_reads'.format( type = type_string ) )
                    tsv_header.append( 'flagstat_{type}_QC-failed_reads'.format( type = type_string ) )
                    match = number_target.search( line )
                    if match:
                        tsv_values.append( match.group( 1 ) )
                        tsv_values.append( match.group( 2 ) )
                    else:
                        tsv_values.append( 0 )
                        tsv_values.append( 0 )
    
                    if match_ratio:
                        tsv_header.append( 'flagstat_{type}_ratio'.format( type = type_string ) )
                        tsv_values.append( match_ratio.group( 1 ) )
    
            # No.5 coverage.py
            elif line_split[ 0 ] == 'non-N_total_depth':
                f_type = 'coverage_data'
                tsv_header += line_split
                        
            elif f_type == 'coverage_data':
                tsv_values +=line_split
                f_type = ''
    
        #
        # Make Excel file
        #
        wb = xlwt.Workbook()
        ws = wb.add_sheet('data')
    
        num_readgroup = len( bam_stats )
        for i in range( 0, len( tsv_header ) ):
            ws.write(0, i, tsv_header[ i ] )
    
            if tsv_header[ i ] == 'readgroup':
                ws.write( 1, i, "*" )
    
            elif tsv_header[ i ] in [
                                      #'readgroup', 
                                      #'read_length_r1',
                                      #'read_length_r2',
                                      '#_mapped_bases',
                                      '#_mapped_bases_r1',
                                      '#_mapped_bases_r2',
                                      '#_divergent_bases',
                                      '#_divergent_bases_r1',
                                      '#_divergent_bases_r2',
                                      '#_total_reads',
                                      '#_total_reads_r1',
                                      '#_total_reads_r2',
                                      '#_mapped_reads',
                                      '#_mapped_reads_r1',
                                      '#_mapped_reads_r2',
                                      '#_mapped_reads_properly_paired',
                                      '#_gc_bases_r1',
                                      '#_gc_bases_r2',
                                      #'mean_insert_size',
                                      #'insert_size_sd',
                                      #'median_insert_size',
                                      '#_duplicate_reads',
                                      #"average_depth",
                                      #"depth_stdev",
                                      #"non-N_total_depth",
                                      #"total_bases",
                                      #"non-N_bases",
                                      #"2x",
                                      #"2x_ratio",
                                      #"10x",
                                      #"10x_ratio",
                                      #"20x",
                                      #"20x_ratio",
                                      #"30x",
                                      #"30x_ratio",
                                      #"40x",
                                      #"40x_ratio",
                                      #"50x",
                                      #"50x_ratio",
                                      #"100x",
                                      #"100x_ratio"
                                     ]:
    
                ws.write( 1, i, xlwt.Formula( 'sum({start_col}{start_row}:{end_col}{end_row})'.format(
                                            start_col = self.ToExcelString( i + 1),
                                            start_row = 3,
                                            end_col = self.ToExcelString( i + 1 ),
                                            end_row = num_readgroup + 3 - 1 ) ) )
    
            elif tsv_header[ i ] in [
                                      'mean_insert_size',
                                      'insert_size_sd',
                                      'median_insert_size' ]:
    
                ws.write( 1, i, xlwt.Formula( 'average({start_col}{start_row}:{end_col}{end_row})'.format(
                                            start_col = self.ToExcelString( i + 1),
                                            start_row = 3,
                                            end_col = self.ToExcelString( i + 1 ),
                                            end_row = num_readgroup + 3 - 1 ) ) )
    
            elif tsv_header[ i ] in [
                                      #'readgroup', 
                                      'read_length_r1',
                                      'read_length_r2',
                                      #'#_mapped_bases',
                                      #'#_mapped_bases_r1',
                                      #'#_mapped_bases_r2',
                                      #'#_divergent_bases',
                                      #'#_divergent_bases_r1',
                                      #'#_divergent_bases_r2',
                                      #'#_total_reads',
                                      #'#_total_reads_r1',
                                      #'#_total_reads_r2',
                                      #'#_mapped_reads',
                                      #'#_mapped_reads_r1',
                                      #'#_mapped_reads_r2',
                                      #'#_mapped_reads_properly_paired',
                                      #'#_gc_bases_r1',
                                      #'#_gc_bases_r2',
                                      #'mean_insert_size',
                                      #'insert_size_sd',
                                      #'median_insert_size',
                                      #'#_duplicate_reads',
                                      #"average_depth",
                                      #"depth_stdev",
                                      'flagstat_total_QC-passed_reads', 
                                      'flagstat_total_QC-failed_reads', 
                                      'flagstat_secondary_QC-passed_reads', 
                                      'flagstat_secondary_QC-failed_reads', 
                                      'flagstat_supplementary_QC-passed_reads', 
                                      'flagstat_supplementary_QC-failed_reads', 
                                      'flagstat_duplicates_QC-passed_reads', 
                                      'flagstat_duplicates_QC-failed_reads', 
                                      'flagstat_mapped_QC-passed_reads', 
                                      'flagstat_mapped_QC-failed_reads', 
                                      #'flagstat_mapped_ratio', 
                                      'flagstat_paired_QC-passed_reads', 
                                      'flagstat_paired_QC-failed_reads', 
                                      'flagstat_read1_QC-passed_reads', 
                                      'flagstat_read1_QC-failed_reads', 
                                      'flagstat_read2_QC-passed_reads', 
                                      'flagstat_read2_QC-failed_reads', 
                                      'flagstat_properly_paired_QC-passed_reads', 
                                      'flagstat_properly_paired_QC-failed_reads', 
                                      #'flagstat_properly_paired_ratio', 
                                      'flagstat_mapped_QC-passed_reads', 
                                      'flagstat_mapped_QC-failed_reads', 
                                      'flagstat_singletons_QC-passed_reads', 
                                      'flagstat_singletons_QC-failed_reads', 
                                      #'flagstat_singletons_ratio', 
                                      'flagstat_mapped_QC-passed_reads', 
                                      'flagstat_mapped_QC-failed_reads', 
                                      'flagstat_mapped_QC-passed_reads', 
                                      'flagstat_mapped_QC-failed_reads', 
                                      "non-N_total_depth",
                                      "total_bases",
                                      "non-N_bases",
                                      "2x",
                                      #"2x_ratio",
                                      "10x",
                                      #"10x_ratio",
                                      "20x",
                                      #"20x_ratio",
                                      "30x",
                                      #"30x_ratio",
                                      "40x",
                                      #"40x_ratio",
                                      "50x",
                                      #"50x_ratio",
                                      "100x",
                                      #"100x_ratio"
                                     ]:
                ws.write( 1, i, int( float( tsv_values[ i ] ) ) )
    
            elif tsv_header[ i ] in [
                                      #'readgroup', 
                                      #'read_length_r1',
                                      #'read_length_r2',
                                      #'#_mapped_bases',
                                      #'#_mapped_bases_r1',
                                      #'#_mapped_bases_r2',
                                      #'#_divergent_bases',
                                      #'#_divergent_bases_r1',
                                      #'#_divergent_bases_r2',
                                      #'#_total_reads',
                                      #'#_total_reads_r1',
                                      #'#_total_reads_r2',
                                      #'#_mapped_reads',
                                      #'#_mapped_reads_r1',
                                      #'#_mapped_reads_r2',
                                      #'#_mapped_reads_properly_paired',
                                      #'#_gc_bases_r1',
                                      #'#_gc_bases_r2',
                                      #'mean_insert_size',
                                      #'insert_size_sd',
                                      #'median_insert_size',
                                      #'#_duplicate_reads',
                                      'average_depth',
                                      'depth_stdev',
                                      'flagstat_mapped_ratio', 
                                      'flagstat_properly_paired_ratio', 
                                      'flagstat_singletons_ratio', 
                                      #"non-N_total_depth",
                                      #"total_bases",
                                      #"non-N_bases",
                                      #"2x",
                                      "2x_ratio",
                                      #"10x",
                                      "10x_ratio",
                                      #"20x",
                                      "20x_ratio",
                                      #"30x",
                                      "30x_ratio",
                                      #"40x",
                                      "40x_ratio",
                                      #"50x",
                                      "50x_ratio",
                                      #"100x",
                                      "100x_ratio"
                                     ]:
                ws.write( 1, i, float( tsv_values[ i ] ) )
    
            else:
                ws.write( 1, i, tsv_values[ i ] )
    
    
        for i in range( 0, num_readgroup ):
            for j in range( 0, len( bam_stats[ i ] ) ):
                if bam_stats_header[ j ] in [
                                      #'readgroup', 
                                      'read_length_r1',
                                      'read_length_r2',
                                      '#_mapped_bases',
                                      '#_mapped_bases_r1',
                                      '#_mapped_bases_r2',
                                      '#_divergent_bases',
                                      '#_divergent_bases_r1',
                                      '#_divergent_bases_r2',
                                      '#_total_reads',
                                      '#_total_reads_r1',
                                      '#_total_reads_r2',
                                      '#_mapped_reads',
                                      '#_mapped_reads_r1',
                                      '#_mapped_reads_r2',
                                      '#_mapped_reads_properly_paired',
                                      '#_gc_bases_r1',
                                      '#_gc_bases_r2',
                                      #'mean_insert_size',
                                      #'insert_size_sd',
                                      #'median_insert_size',
                                      '#_duplicate_reads'
    
                                      ]:
                    ws.write( i + 2, j, int( bam_stats[ i ][ j ] ) )
    
                elif bam_stats_header[ j ] in [
                                      #'readgroup', 
                                      #'read_length_r1',
                                      #'read_length_r2',
                                      #'#_mapped_bases',
                                      #'#_mapped_bases_r1',
                                      #'#_mapped_bases_r2',
                                      #'#_divergent_bases',
                                      #'#_divergent_bases_r1',
                                      #'#_divergent_bases_r2',
                                      #'#_total_reads',
                                      #'#_total_reads_r1',
                                      #'#_total_reads_r2',
                                      #'#_mapped_reads',
                                      #'#_mapped_reads_r1',
                                      #'#_mapped_reads_r2',
                                      #'#_mapped_reads_properly_paired',
                                      #'#_gc_bases_r1',
                                      #'#_gc_bases_r2',
                                      'mean_insert_size',
                                      'insert_size_sd',
                                      'median_insert_size',
                                      #'#_duplicate_reads'
                                      ]:
                    ws.write( i + 2, j, float( bam_stats[ i ][ j ] ) )
    
                else:
                    ws.write( i + 2, j, bam_stats[ i ][ j ] )
                
    
        wb.save( excel_file )
   
    
    def Excel2TSV(self, ExcelFile, TSVFile):
         import xlrd
         workbook = xlrd.open_workbook(ExcelFile)
         worksheet = workbook.sheet_by_name('data')
         tsvfile = open(TSVFile, 'wb')
    
         for rownum in xrange(worksheet.nrows):
             data_to_write = []
             for x in worksheet.row_values(rownum):
                 if isinstance( x, basestring ):
                     x = x.replace( "\t", "")
                 if type( x ) == type( u'' ):
                     data_to_write.append( x.encode('utf-8') )
                 else:
                     data_to_write.append( str( x ) )
    
             tsvfile.write( '\t'.join( data_to_write ) + '\n' )
    
    #         wr.writerow(
    #             list(x.encode('utf-8') if type(x) == type(u'') else x
    #                  for x in worksheet.row_values(rownum)))
    
         tsvfile.close()
    
    
