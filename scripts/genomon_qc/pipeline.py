import os

from ruffus import *
from genomon_qc.config.run_conf import *
from genomon_qc.config.genomon_conf import *
from genomon_qc.config.sample_conf import *
from genomon_qc.resource.qc_bamstats import *
from genomon_qc.resource.qc_coverage import *
from genomon_qc.resource.qc_merge import *

# set task classes
r_qc_bamstats = Res_QC_Bamstats(genomon_conf.get("qc_bamstats", "qsub_option"), run_conf.project_root + '/script')
r_qc_coverage = Res_QC_Coverage(genomon_conf.get("qc_coverage", "qsub_option"), run_conf.project_root + '/script')
r_qc_merge = Res_QC_Merge(genomon_conf.get("qc_merge", "qsub_option"), run_conf.project_root + '/script')

# prepare output directories
if not os.path.isdir(run_conf.project_root): os.mkdir(run_conf.project_root)
if not os.path.isdir(run_conf.project_root + '/script'): os.mkdir(run_conf.project_root + '/script')
if not os.path.isdir(run_conf.project_root + '/log'): os.mkdir(run_conf.project_root + '/log')
if not os.path.isdir(run_conf.project_root + '/bam'): os.mkdir(run_conf.project_root + '/bam')
if not os.path.isdir(run_conf.project_root + '/qc'): os.mkdir(run_conf.project_root + '/qc')

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
# qc stage
@follows( link_import_bam )
@transform(link_import_bam, formatter("(.bam)$"),
           "{subpath[0][2]}/qc/{subdir[0][0]}/{basename[0]}.bamstats"
           )
def bam_stats(input_file, output_file):

    dir_name = os.path.dirname(output_file)
    if not os.path.exists(dir_name): os.makedirs(dir_name)
     
    arguments = {"PCAP": genomon_conf.get("SOFTWARE", "PCAP"),
                 "PERL5LIB": genomon_conf.get("ENV", "PERL5LIB"),
                 "input": input_file,
                 "output": output_file,
                 "log": run_conf.project_root + '/log'}

    r_qc_bamstats.task_exec(arguments) 

@follows( link_import_bam )
@transform(link_import_bam, formatter("(.bam)$"),
           "{subpath[0][2]}/qc/{subdir[0][0]}/{basename[0]}.coverage"
           )
def coverage(input_file, output_file):
   
    dir_name = os.path.dirname(output_file)
    if not os.path.exists(dir_name): os.makedirs(dir_name)
    sample_name = os.path.basename(dir_name)
    depth_output_file = dir_name+'/'+sample_name+'.depth'
    
    incl_bed_file = ""
    genome_file = ""
    if run_conf.analysis_type == "wgs":
        genome_file = genomon_conf.get("REFERENCE", "hg19_genome")
        incl_bed_file = output_file + "genome.bed"
        incl_bed_w = genomon_conf.get("qc_coverage", "wgs_incl_bed_width")
        r_qc_coverage.create_incl_bed_wgs(genome_file, incl_bed_file, int(incl_bed_w), "")

    arguments = {"data_type": run_conf.analysis_type,
                 "i_bed_lines": genomon_conf.get("qc_coverage", "wgs_i_bed_lines"),
                 "i_bed_size": genomon_conf.get("qc_coverage", "wgs_i_bed_width"),
                 "incl_bed_file": incl_bed_file,
                 "genome_file": genome_file,
                 "gaptxt": genomon_conf.get("REFERENCE", "gaptxt"),
                 "bait_file": genomon_conf.get("REFERENCE", "bait_file"),
                 "BEDTOOLS": genomon_conf.get("SOFTWARE", "bedtools"),
                 "SAMTOOLS": genomon_conf.get("SOFTWARE", "samtools"),
                 "LD_LIBRARY_PATH": genomon_conf.get("ENV", "LD_LIBRARY_PATH"),
                 "input": input_file,
                 "output": depth_output_file,
                 "log": run_conf.project_root + '/log'}

    r_qc_coverage.task_exec(arguments)
    r_qc_coverage.calc_coverage(depth_output_file, genomon_conf.get("qc_coverage", "coverage"), output_file)
    
    os.unlink(dir_name+'/'+sample_name+'.depth')
    os.unlink(dir_name+'/'+sample_name+'.depth.input_bed')
   
###################
# merge stage

@follows( bam_stats )
@follows( coverage )

@collate([bam_stats, coverage], formatter(""),
           "{subpath[0][2]}/qc/{subdir[0][0]}/{basename[0]}.genomonQC.result.filt.txt")
def merge_qc(input_files, output_file):

    r_qc_merge.write_qc(input_files, output_file, get_meta_info(["genomon_qc"]))

