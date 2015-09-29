# GenomonSummary

script for calculating summary

## Dependency

 - Python (>= 2.7), pysam, numpy, xlrd, xlwt
 - samtools
 - bedtools
 - PCAP-core

## Install & Run

Download all files in this repository

```
$ git clone https://github.com/aokad/bamstats.git
$ cd bamstat
```

Download and setting

```
$ mkdir data
$ cd data
$ wget http://hgdownload.soe.ucsc.edu/goldenPath/hg19/database/gap.txt.gz
$ gunzip gap.txt.gz
```

Write setting, your environment

```
$ cd ..
$ vi bamstats.sh
sureselect={your bed file path}
```

Run.

```
# exome
$ ./bamstats.sh ${input bam file} ${output txt file} exome

# wgs
$ ./bamstats.sh ${input bam file} ${output txt file} wgs
```

Run multi files (use qsub).

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

