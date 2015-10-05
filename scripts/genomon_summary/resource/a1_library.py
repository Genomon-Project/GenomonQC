#! /usr/bin/env python

from genomon_summary.stage_task import *

class Res_A1library(Stage_task):

    task_name = "a1_library"

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

# MET_FILE=`echo {input} | sed 's/\.bam/.metrics/'`
MET_FILE=`echo {input}.metrics`
grep -A1 LIBRARY $MET_FILE > {output}
"""

    def __init__(self, qsub_option, script_dir):
        super(Res_A1library, self).__init__(qsub_option, script_dir)
