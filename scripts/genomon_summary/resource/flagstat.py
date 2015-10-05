#! /usr/bin/env python

from genomon_summary.stage_task import *

class Res_Flagstat(Stage_task):

    task_name = "flagstat"

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

echo "samtools_flagstat" > {output}
{SAMTOOLS} flagstat {input} >> {output}
"""

    def __init__(self, qsub_option, script_dir):
        super(Res_Flagstat, self).__init__(qsub_option, script_dir)
