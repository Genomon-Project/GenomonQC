# -*- coding: utf-8 -*-
"""
Created on Thu Oct 20 13:59:56 2016

@author: okada
"""

def run(args):
    
    import subprocess
    
    cmd_template = """
#!/bin/bash
#
# Set SGE
#
#$ -S /bin/bash         # set shell in UGE
#$ -cwd                 # execute at the submitted dir
pwd                     # print current working directory
hostname                # print hostname
date                    # print date
set -xv

export PERL5LIB={PERL5LIB}

{bamstats} -i {input} -o {output}.tmp || exit $?
mv {output}.tmp {output}
"""

    cmd = cmd_template.format(PERL5LIB = args.perl5lib,
                            bamstats = args.bamstats,
                            input = args.input_file,
                            output = args.output_file)

    subprocess.check_call(cmd, shell=True)

if __name__ == "__main__":
    pass

