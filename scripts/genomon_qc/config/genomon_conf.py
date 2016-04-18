#! /usr/bin/env python

import sys, os, pwd, subprocess, ConfigParser
from genomon_pipeline.__init__ import __version__
from genomon_pipeline.config.genomon_conf import *
from genomon_pipeline.config.run_conf import *

global genomon_conf

genomon_conf = ConfigParser.SafeConfigParser()

software_version ={'genomon_pipeline':'genomon_pipeline-'+__version__}

dna_reference_list = ["hg19_genome",
                      "gaptxt",
                      "bait_file"
                      ]
           
dna_software_list = ["samtools",
                     "bedtools",
                     "PCAP"
                     ]

err_msg = 'No target File : \'%s\' for the %s key in the section of %s' 


def dna_genomon_conf_check():
    """
    function for checking the validity of genomon_conf for DNA analysis
    """

    section = "REFERENCE"
    for key in dna_reference_list:

        if key == "inhouse_normal_tabix_db":
            if genomon_conf.has_option("annotation", "active_inhouse_normal_flag"):
                flag = genomon_conf.get("annotation", "active_inhouse_normal_flag")
                if flag == "True":
                    value = genomon_conf.get(section, key)
                    if not os.path.exists(value):
                        raise ValueError(err_msg % (value, key, section))
            continue
        
        if key == "inhouse_tumor_tabix_db":
            if genomon_conf.has_option("annotation", "active_inhouse_tumor_flag"):
                flag = genomon_conf.get("annotation", "active_inhouse_tumor_flag")
                if flag == "True":
                    value = genomon_conf.get(section, key)
                    if not os.path.exists(value):
                        raise ValueError(err_msg % (value, key, section))
            continue
            
        if key == "HGVD_tabix_db":
            if genomon_conf.has_option("annotation", "active_HGVD_flag"):
                flag = genomon_conf.get("annotation", "active_HGVD_flag")
                if flag == "True":
                    value = genomon_conf.get(section, key)
                    if not os.path.exists(value):
                        raise ValueError(err_msg % (value, key, section))
            continue
            
        if key == "HGMD_tabix_db":
            if genomon_conf.has_option("annotation", "active_HGMD_flag"):
                flag = genomon_conf.get("annotation", "active_HGMD_flag")
                if flag == "True":
                    value = genomon_conf.get(section, key)
                    if not os.path.exists(value):
                        raise ValueError(err_msg % (value, key, section))
            continue
            
        value = genomon_conf.get(section, key)
        if not os.path.exists(value):
            raise ValueError(err_msg % (value, key, section))

    section = "SOFTWARE"
    for key in dna_software_list:
        
        if key == "annovar":
            if genomon_conf.has_option("annotation", "active_annovar_flag"):
                flag = genomon_conf.get("annotation", "active_annovar_flag")
                if flag == "True":
                    value = genomon_conf.get(section, key)
                    if not os.path.exists(value):
                        raise ValueError(err_msg % (value, key, section))
            continue
            
        value = genomon_conf.get(section, key)
        if not os.path.exists(value):
            raise ValueError(err_msg % (value, key, section))

    pass


def get_meta_info(softwares):

    print_meta_info = "# Version: GenomonQC 1.1.0"
    print_meta_info = print_meta_info + '\n' + "# Analysis Date: " + run_conf.analysis_date
    print_meta_info = print_meta_info + '\n' + "# User: " + pwd.getpwuid(os.getuid()).pw_name
   
    return print_meta_info

