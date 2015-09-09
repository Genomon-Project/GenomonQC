#!/bin/bash
#
#$ -S /bin/bash
#$ -cwd
#$ -e ./log
#$ -o ./log

BAM=${1}
OUT=${2}

##### configure
# PCAP
export PERL5LIB=/home/w3varann/.local/lib/perl/lib/perl5/:/home/w3varann/.local/lib/perl/lib/
PCAP=/home/w3varann/tools/PCAP-core-dev.20150511

# python
SCRIPT=./python
export PYTHONPATH=$PYTHONPATH:${SCRIPT}:/home/w3varann/.local/lib/python2.7/site-packages
export PYTHONHOME=/usr/local/package/python2.7/current
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:${PYTHONHOME}/lib

# samtools
SAMTOOLS=/home/w3varann/tools/samtools-1.2/samtools

# bedtools
BEDTOOLS=/home/w3varann/tools/bedtools-2.24.0/bin/bedtools

# coverage
bed_file=/home/aiokada/work/bamstat/db/SureSelect50M.picard
coverage='2,10,20,30,40,50,100'
process_num=10
sampling_num=1000

##### bam_stats_calc

: <<'#COMMENT'
## bam_stats
${PCAP}/bin/bam_stats.pl -i ${BAM} -o ${OUT}.1

## grep -A1 LIBRARY
MET_FILE=`echo ${BAM} | sed 's/\.bam/.metrics/'`
grep -A1 LIBRARY $MET_FILE > ${OUT}.2

## samtools flagstat
echo "samtools_flagstat" > ${OUT}.3
${SAMTOOLS} flagstat ${BAM} >> ${OUT}.3


## coverage.py
total_l=`cat ${bed_file}.bed | wc -l`
header_l=`grep ^@ ${bed_file}.bed | wc -l`
data_l=`expr $total_l - $header_l`
tail -$data_l ${bed_file}.bed > ${bed_file}.noheader.bed
${BEDTOOLS} sort -i ${bed_file}.noheader.bed > ${bed_file}.sort.bed
${BEDTOOLS} merge -i ${bed_file}.sort.bed > ${bed_file}.merge.bed

#COMMENT
/usr/local/package/python2.7/current/bin/python ${SCRIPT}/coverage.py -i ${BAM} -t ${OUT}.depth -e ${bed_file}.merge.bed -n ${sampling_num} -p ${process_num} -c ${coverage} -s ${SAMTOOLS} > ${OUT}.4

##### bam_stats_merge

OUT_TSV=`echo ${OUT} | sed 's/\.txt/.tsv/'`
OUT_XLS=`echo ${OUT} | sed 's/\.txt/.xls/'`
cat ${OUT}.1 ${OUT}.2 ${OUT}.3 ${OUT}.4 > ${OUT}
/usr/local/package/python2.7/current/bin/python ${SCRIPT}/mkxls.py -i ${OUT} -x $OUT_XLS
/usr/local/package/python2.7/current/bin/python ${SCRIPT}/xl2tsv.py -t $OUT_TSV -x $OUT_XLS




