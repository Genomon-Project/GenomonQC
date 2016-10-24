# -*- coding: utf-8 -*-
"""
Created on Thu Oct 20 12:03:45 2016

@author: okada
"""

import os

class InputError(Exception):
    """Exception raised for errors in the input.

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    #def __init__(self, expression, message):
    def __init__(self, message):
        #self.expression = expression
        self.message = message

def load_config(config_file):
    import sys

    if len(config_file) == 0:
        return None
    
    if os.path.exists(config_file) == False:
        return None
        
    if sys.version_info.major == 3:
        import configparser as cp
    else:
        import ConfigParser as cp

    config = cp.RawConfigParser()
    config.read(config_file)

    return config

def path_check(path, arg_name):
    if os.path.exists(path) == False:
        raise InputError ("[InputError] File is not exist. %s (%s)" % (path, arg_name))

def config_get(arg, arg_name, config, section, item, default, type):
    
    value = arg
    
    if arg == default:
        if config == None:
            raise InputError ("[InputError] Command option '%s' is unspecified, specify this, or use '--config_file' option. [%s] %s" % (arg_name, section, item))
            
        if config.has_option(section, item) == False:
            raise InputError ("[InputError] Config file does not have this option. [%s] %s" % (section, item))
        
        if type == 'int':
            value = config.getint(section, item)
        else:
            value = config.get(section, item)

    if type == 'path':
        path_check(value, arg_name)

    return value

def wgs_main(args):
    import genomon_qc.coverage as coverage
    
    path_check(args.input_file, "input_file")
    
    output_dir = os.path.dirname(args.output_file)
    if os.path.exists(output_dir) == False:
        os.mkdir(output_dir)
    
    config = load_config(args.config_file)
    args.genome_size_file = config_get(args.genome_size_file, "--genome_size_file", config, "REFERENCE", "hg19_genome", "", "path")
    args.gaptxt           = config_get(args.gaptxt, "--gaptxt", config, "REFERENCE", "gaptxt", "", "path")
    args.incl_bed_width   = config_get(args.incl_bed_width, "--incl_bed_width", config, "qc_coverage", "wgs_incl_bed_width", -1, "int")
    args.i_bed_lines      = config_get(args.i_bed_lines, "--i_bed_lines", config, "qc_coverage", "wgs_i_bed_lines", -1, "int")
    args.i_bed_width      = config_get(args.i_bed_width, "--i_bed_width", config, "qc_coverage", "wgs_i_bed_width", -1, "int")
    args.ld_library_path  = config_get(args.ld_library_path, "--ld_library_path", config, "ENV", "LD_LIBRARY_PATH", "", "str")
    args.bedtools         = config_get(args.bedtools, "--bedtools", config, "SOFTWARE", "bedtools", "", "path")
    args.samtools         = config_get(args.samtools, "--samtools", config, "SOFTWARE", "samtools", "", "path")
    args.samtools_params  = config_get(args.samtools_params, "--samtools_params", config, "qc_coverage", "samtools_params", "", "str")
    args.coverage_text    = config_get(args.coverage_text, "--coverage_text", config, "qc_coverage", "coverage", "", "str")
    
    coverage.run_wgs(args)

def exome_main(args):
    import genomon_qc.coverage as coverage
    
    path_check(args.input_file, "input_file")
    
    output_dir = os.path.dirname(args.output_file)
    if os.path.exists(output_dir) == False:
        os.mkdir(output_dir)
    
    config = load_config(args.config_file)
    args.bait_file        = config_get(args.bait_file, "--bait_file", config, "REFERENCE", "bait_file", "", "path")
    args.ld_library_path  = config_get(args.ld_library_path, "--ld_library_path", config, "ENV", "LD_LIBRARY_PATH", "", "str")
    args.bedtools         = config_get(args.bedtools, "--bedtools", config, "SOFTWARE", "bedtools", "", "path")
    args.samtools         = config_get(args.samtools, "--samtools", config, "SOFTWARE", "samtools", "", "path")
    args.samtools_params  = config_get(args.samtools_params, "--samtools_params", config, "qc_coverage", "samtools_params", "", "str")
    args.coverage_text    = config_get(args.coverage_text, "--coverage_text", config, "qc_coverage", "coverage", "", "str")
    
    coverage.run_exome(args)
    
def bamstats_main(args):
    import genomon_qc.bamstats as bamstats
    
    path_check(args.input_file, "input_file")
    
    output_dir = os.path.dirname(args.output_file)
    if os.path.exists(output_dir) == False:
        os.mkdir(output_dir)
        
    config = load_config(args.config_file)
    args.perl5lib = config_get(args.perl5lib, "--perl5lib", config, "ENV", "PERL5LIB", "", "str")
    args.bamstats = config_get(args.bamstats, "--bamstats", config, "SOFTWARE", "bamstats", "", "path")
    
    bamstats.run(args)

def merge_main(args):
    import genomon_qc.merge as merge
    
    path_check(args.coverage_file, "coverage_file")
    path_check(args.bamstats_file, "bamstats_file")
    
    output_dir = os.path.dirname(args.output_file)
    if os.path.exists(output_dir) == False:
        os.mkdir(output_dir)
    
    merge.run(args.bamstats_file, args.coverage_file, args.output_file, args.meta)
    
