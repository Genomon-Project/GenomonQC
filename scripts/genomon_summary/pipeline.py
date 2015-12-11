import os

from ruffus import *
from genomon_summary.config.run_conf import *
from genomon_summary.config.genomon_conf import *
from genomon_summary.config.task_conf import *
from genomon_summary.config.sample_conf import *
from genomon_summary.resource.bam_stats import *
from genomon_summary.resource.coverage import *
from genomon_summary.resource.merge import *

# set task classes
r_bamstats = Res_Bamstats(task_conf.get("bam_stats", "qsub_option"), run_conf.project_root + '/script')
r_coverage = Res_Coverage(task_conf.get("coverage", "qsub_option"), run_conf.project_root + '/script')
r_merge = Res_Merge(task_conf.get("merge", "qsub_option"), run_conf.project_root + '/script')

# prepare output directories
if not os.path.isdir(run_conf.project_root): os.mkdir(run_conf.project_root)
if not os.path.isdir(run_conf.project_root + '/script'): os.mkdir(run_conf.project_root + '/script')
if not os.path.isdir(run_conf.project_root + '/log'): os.mkdir(run_conf.project_root + '/log')
if not os.path.isdir(run_conf.project_root + '/bam'): os.mkdir(run_conf.project_root + '/bam')
if not os.path.isdir(run_conf.project_root + '/summary'): os.mkdir(run_conf.project_root + '/summary')

link_list = []
for sample in sample_conf.bam_import:
    link_list.append(run_conf.project_root + '/bam/' + sample +'/'+ sample +'.bam')
            
############################
# link the import bam files
@originate(link_list)
def link_import_bam(output_file):

    link_dir = os.path.dirname(output_file)
    if not os.path.isdir(link_dir): os.mkdir(link_dir)
        
    sample, ext = os.path.splitext(os.path.basename(output_file))
    bam = sample_conf.bam_import[sample]
    if os.path.exists(output_file): os.remove(output_file)
    os.symlink(bam, output_file)
        
    bam_prefix, ext = os.path.splitext(bam)   
    if os.path.exists(output_file +'.bai'): os.remove(output_file +'.bai')
    if (os.path.exists(bam +'.bai')):
        os.symlink(bam +'.bai', output_file +'.bai')
    elif (os.path.exists(bam_prefix +'.bai')):
        os.symlink(bam_prefix +'.bai', output_file +'.bai')

###################
# summary stage
@transform(link_import_bam, formatter("(.bam)$"),
           "{subpath[0][2]}/summary/{subdir[0][0]}/{basename[0]}.bamstats"
           )
def bam_stats(input_file, output_file):

    dir_name = os.path.dirname(output_file)
    if not os.path.exists(dir_name): os.makedirs(dir_name)
     
    arguments = {"PCAP": genomon_conf.get("SOFTWARE", "PCAP"),
                 "PERL5LIB": genomon_conf.get("ENV", "PERL5LIB"),
                 "input": input_file,
                 "output": output_file,
                 "log": run_conf.project_root + '/log'}

    r_bamstats.task_exec(arguments) 

@transform(link_import_bam, formatter("(.bam)$"),
           "{subpath[0][2]}/summary/{subdir[0][0]}/{basename[0]}.depth"
           )
def coverage(input_file, output_file):
   
    dir_name = os.path.dirname(output_file)
    if not os.path.exists(dir_name): os.makedirs(dir_name)
    
    incl_bed_file = ""
    genome_file = ""
    if run_conf.analysis_type == "wgs":
        genome_file = genomon_conf.get("REFERENCE", "hg19_genome")
        incl_bed_file = output_file + "genome.bed"
        incl_bed_w = task_conf.get("coverage", "wgs_incl_bed_width")
        r_coverage.create_incl_bed_wgs(genome_file, incl_bed_file, int(incl_bed_w), "")

    arguments = {"data_type": run_conf.analysis_type,
                 "i_bed_lines": task_conf.get("coverage", "wgs_i_bed_lines"),
                 "i_bed_size": task_conf.get("coverage", "wgs_i_bed_width"),
                 "incl_bed_file": incl_bed_file,
                 "genome_file": genome_file,
                 "gaptxt": genomon_conf.get("REFERENCE", "gaptxt"),
                 "bait_file": genomon_conf.get("REFERENCE", "bait_file"),
                 "BEDTOOLS": genomon_conf.get("SOFTWARE", "bedtools"),
                 "SAMTOOLS": genomon_conf.get("SOFTWARE", "samtools"),
                 "LD_LIBRARY_PATH": genomon_conf.get("ENV", "LD_LIBRARY_PATH"),
                 "input": input_file,
                 "output": output_file,
                 "log": run_conf.project_root + '/log'}

    r_coverage.task_exec(arguments)

@transform(coverage, suffix(".depth"), ".coverage")
def coverage_calc(input_file, output_file):
    r_coverage.calc_coverage(input_file, task_conf.get("coverage", "coverage"), output_file)
    
###################
# merge stage
@collate([bam_stats, coverage_calc], formatter(""),
           "{subpath[0][2]}/summary/{subdir[0][0]}/{basename[0]}.tsv"
           )
def merge(input_files, output_file):

    for f in input_files:
        if not os.path.exists(f):
            raise

    input_split = os.path.splitext(input_files[0])
    output_split = os.path.splitext(output_file)
    files = []
    files.append(input_split[0] + ".bamstats")
    files.append(input_split[0] + ".coverage")
    excel_file = output_split[0] + ".xls"
    r_merge.mkxls(files, excel_file)
    r_merge.Excel2TSV(excel_file, output_file)


