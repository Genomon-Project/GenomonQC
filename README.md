# GenomonSummary

script for calculating summary

## Dependency

 - Python (>= 2.7), pysam, pynum, xlrd, xlwt
 - samtools
 - PCAP-core

## Install & Run

Dounload all files in this repository

```
$ git clone https://github.com/aokad/bamstats.git
$ cd bamstat
```

Run.

```
$ ./bamstats.sh ${input bam file}.bam ${output txt file}.txt
```

Run multi files(use qsub).

```
$ qsub ./bamstats.sh ${input bam file 1}.bam ${output txt file 1}.txt
$ qsub ./bamstats.sh ${input bam file 2}.bam ${output txt file 2}.txt
$ qsub ./bamstats.sh ${input bam file 3}.bam ${output txt file 3}.txt
$ qsub ./bamstats.sh ${input bam file 4}.bam ${output txt file 4}.txt
$ qsub ./bamstats.sh ${input bam file 5}.bam ${output txt file 5}.txt
```


## Directory

```
{repository root}
 |- README.md           # this file
 |- bamstats.sh         # run script
 |- [DIR] python        # python scripts
 |- [DIR] log           # log files
 ~
 
 {output dir}
 |- {output txt file}.txt         # above your write
 |- {output txt file}.txt.1       # temporary file
 |- {output txt file}.txt.2       # temporary file
 |- {output txt file}.txt.3       # temporary file
 |- {output txt file}.txt.4       # temporary file
 |                                # {output txt file}.txt to create, concatenates temporary file 1 ~ 4.
 |
 |- {output txt file}.tsv         # ★result file with tab separation
 |- {output txt file}.xls         # ★result file (EXCEL)
 
```
