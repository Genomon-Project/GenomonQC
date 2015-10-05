#! /usr/bin/env python

import os
from genomon_summary.config.run_conf import *

class Sample_conf(object):

    def __init__(self):

        self.bam_import = {}

        # 
        # should add the file exist check here ?
        #
    

    def parse_file(self, file_path):

        file_ext = os.path.splitext(file_path)[1]

        file_data = []
        if file_ext.lower() == '.csv':
            file_data = self.parse_csv(file_path)
        elif file_ext.lower() == '.txt' or file_ext.lower() == '.tsv':
            file_data = self.parse_tsv(file_path)
        # elif file_ext.lower() == '.xlsx':
            # file_data = self.parse_xlsx(file_path)
        else:
            # 
            # should treat other cases ??
            #
            raise NotImplementedError("currently, we can just accept tsv and csv formats")
 

        file_data_trimmed = []
        for line_data in file_data:
       
            # skip empty lines
            if len(line_data) == 0: continue
 
            # line starting with '#' is comment
            if line_data[0].startswith('#'): continue
             
            # remove spaces
            line_data = map(lambda x: x.strip(' '), line_data)

            # skip if all the elements are empty
            if len(line_data) == line_data.count(''): continue

            file_data_trimmed.append(line_data)


        self.parse_data(file_data_trimmed)


    def parse_csv(self, file_path):

        _file_data = []
        import csv
        with open(file_path, 'r') as hIN:
            csv_obj = csv.reader(hIN)
            for cells in csv_obj:
                tempdata = []
                for cell in cells:
                    tempdata.append(cell)
                _file_data.append(tempdata)
    
        return _file_data


    def parse_tsv(self, file_path):

        _file_data = []
        with open(file_path, 'r') as hIN:
            for line in hIN:
                F = line.rstrip('\n').split('\t')
                _file_data.append(F)

        return _file_data


    def parse_data(self, _data ):
    
        mode = ''
        
        sampleID_list = []
        for row in _data:
            if row[0].startswith('['):

                # header
                if row[0].lower() == '[bam_import]':
                    mode = 'bam_import'
                    continue

                else:
                    err_msg = "Section name should be [bam_import]. " + \
                              "Also, sample name should not start with '['."
                    raise ValueError(err_msg)
            
            
            # section data
            if mode == 'bam_import':

                sampleID = row[0]
                # 'None' is presereved for special string
                if sampleID == 'None':
                    err_msg = "None can not be used as sampleID"
                    raise ValueError(err_msg)

                if sampleID in sampleID_list:
                    err_msg = sampleID + " is duplicated."
                    raise ValueError(err_msg)

                sampleID_list.append(sampleID)

                sequence = row[1]
                if not os.path.exists(sequence):
                    err_msg = sampleID + ": " + sequence +  " does not exists"
                    raise ValueError(err_msg)
                
                sequence_prefix, ext = os.path.splitext(sequence)
                if (not os.path.exists(sequence + '.bai')) and (not os.path.exists(sequence_prefix + '.bai')):
                    err_msg = sampleID + ": " + sequence +  " index does not exists"
                    raise ValueError(err_msg)

                self.bam_import[sampleID] = sequence


    # get the paths where bam files imported from another projects will be located"
    def get_linked_bam_import_path(self):
        linked_bam_import_path = []
        for sample in sample_conf.bam_import:
            linked_bam_import_path.append(run_conf.project_root + '/bam/' + sample + '/' + sample + '.bam')
        return linked_bam_import_path

    def sample2bam(self,sample):
        bam = ''
        if (self.bam_import.has_key(sample)):
            bam = run_conf.project_root + '/bam/' + sample + '/' + sample + '.bam'
        else:
            bam = run_conf.project_root + '/bam/' + sample + '/' + sample + '.markdup.bam'
        return bam 

    def get_control_panel_list(self,panel_name):
        control_panel_bam = []
        for sample in self.control_panel[panel_name]:
            control_panel_bam.append(self.sample2bam(sample))
        return control_panel_bam

    def get_disease_and_control_panel_bam(self):
        unique_bams = []
        for complist in sample_conf.compare:
            panel_name = complist[2]
            unique_bams.extend(self.get_control_panel_list(panel_name))
            disease_sample = complist[0]
            unique_bams.append(run_conf.project_root + '/bam/' + disease_sample + '/' + disease_sample + '.markdup.bam')
        result_list = list(set(unique_bams))       
        return result_list

global sample_conf 
sample_conf = Sample_conf()


