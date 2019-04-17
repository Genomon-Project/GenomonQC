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
#set -xv
set -eu
#set -o pipefail

{PERL5LIB}
{PERL}

{bamstats} -i {input} -o {output}.tmp
mv {output}.tmp {output}
"""
    perl5lib = ""
    if args.perl5lib != "":
        perl5lib = "export PERL5LIB=%s" % (args.perl5lib)
    perl = ""
    if args.perl != "":
        perl = "export PATH=%s:$PATH" % (args.perl)

    cmd = cmd_template.format(PERL5LIB = perl5lib,
                            PERL = perl,
                            bamstats = args.bamstats,
                            input = args.input_file,
                            output = args.output_file)

    subprocess.check_call(cmd, shell=True)

if __name__ == "__main__":
    pass

