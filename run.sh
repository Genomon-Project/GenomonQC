#!/bin/bash
#
# Set SGE
#
#$ -S /bin/bash # set shell in UGE
#$ -cwd         # execute at the submitted dir
pwd             # print current working directory
hostname        # print hostname
date            # print date

PYTHONHOME=/usr/local/package/python2.7/current
PYTHONPATH=/home/aiokada/.local/lib/python2.7/site-packages:/home/w3varann/.local/lib/python2.7/site-packages
LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:${PYTHONHOME}/lib:/home/w3varann/.local/lib
R_LIBS=/home/w3varann/.R
R_HOME=/home/w3varann/.R

/usr/local/package/python2.7/current/bin/python genomon_summary $@

