#!/bin/bash
#
#$ -S /bin/bash
#$ -cwd
#$ -e ./log
#$ -o ./log

##### arg
BAM=${1}
OUT=${2}
data_type=${3}    # "wgs" or "exome"

if [ ! -e log ]; then
    mkdir log
fi

output_dir=${OUT%/*}
if [ ! -e ${output_dir} ]; then
    mkdir ${output_dir}
fi

##### configure
# PCAP
export PERL5LIB=/home/w3varann/.local/lib/perl/lib/perl5/:/home/w3varann/.local/lib/perl/lib/
PCAP=/home/w3varann/tools/PCAP-core-dev.20150511

# python
SCRIPT=./python
export PYTHONPATH=$PYTHONPATH:${SCRIPT}:/home/w3varann/.local/lib/python2.7/site-packages
export PYTHONHOME=/usr/local/package/python2.7/current
export LD_LIBRARY_PATH=${PYTHONHOME}/lib:${LD_LIBRARY_PATH}

# samtools
SAMTOOLS=/home/w3varann/tools/samtools-1.2/samtools

# bedtools
BEDTOOLS=/home/w3varann/tools/bedtools-2.24.0/bin/bedtools

# coverage.py
coverage="2,10,20,30,40,50,100"
hg19_genome="/home/w3varann/tools/bedtools-2.24.0/genomes/human.hg19.genome"
gaptxt="./data/gap.txt"
sureselect={your bed file path}

##### bam_stats_calc

## bam_stats
${PCAP}/bin/bam_stats.pl -i ${BAM} -o ${OUT}.1

## grep -A1 LIBRARY
MET_FILE=`echo ${BAM} | sed 's/\.bam/.metrics/'`
grep -A1 LIBRARY $MET_FILE > ${OUT}.2

## samtools flagstat
echo "samtools_flagstat" > ${OUT}.3
${SAMTOOLS} flagstat ${BAM} >> ${OUT}.3

## coverage.py

if [ ${data_type} = "wgs" ]
then
    ########## WGS ##########
    
    # for hg19, create gap text (bedtools shuffle -incl option file)
    genome_file=${hg19_genome}
    bed_file=${OUT}.genome.bed
    /usr/local/package/python2.7/current/bin/python ${SCRIPT}/create_incl_bed_wgs.py -i ${genome_file} -o ${bed_file} -w 1000000 -c ""

    # for hg19, create gap text (bedtools shuffle -excl option file)
    gaptxt_file=${gaptxt}
    gaptxt_cut=${OUT}.gap.txt
    cut -f 2,3,4 ${gaptxt_file} | cut -c 4- > ${gaptxt_cut}

    # create temp bed (bedtools shuffle -i option file)
    lines=10000
    # lines=10
    size=100
    temp_bed=${OUT}_${lines}_${size}.bed
    
    echo '' > ${temp_bed}
    for J in `seq 1 ${lines}`
    do
        printf "1\t0\t%s\n" ${size} >> ${temp_bed}
    done
    
    # bedtools shuffle
    input_bed=${OUT}.input_bed
    ${BEDTOOLS} shuffle -i ${temp_bed} -g ${genome_file} -incl ${bed_file} -excl ${gaptxt_cut} > ${input_bed}

    # rm ${temp_bed} ${bed_file} ${gaptxt_cut}

    # samtools depth's options
    depth_mode="r"            # samtools depth option (-r / -b)

else
    ########## exome ##########

    # merge bed (bedtools shuffle -incl option file)
    bed_file=${sureselect}
    total_l=`cat ${bed_file} | wc -l`
    header_l=`grep ^@ ${bed_file} | wc -l`
    data_l=`expr $total_l - $header_l`
    tail -$data_l ${bed_file} > ${OUT}.noheader.bed
    ${BEDTOOLS} sort -i ${OUT}.noheader.bed > ${OUT}.sort.bed
    ${BEDTOOLS} merge -i ${OUT}.sort.bed > ${OUT}.merge.bed
    cut -c 4- ${OUT}.merge.bed > ${OUT}.merge.cut.bed
    input_bed=${OUT}.merge.cut.bed

    rm ${OUT}.noheader.bed ${OUT}.sort.bed ${OUT}.merge.bed

    # samtools depth's options
    depth_mode="b"            # samtools depth option (-r / -b)

fi

# coverage
/usr/local/package/python2.7/current/bin/python ${SCRIPT}/coverage.py -i ${BAM} -t ${OUT}.depth -e ${input_bed} -c ${coverage} -s ${SAMTOOLS} -m ${depth_mode} > ${OUT}.4

##### bam_stats_merge
OUT_TSV=`echo ${OUT} | sed 's/\.txt/.tsv/'`
OUT_XLS=`echo ${OUT} | sed 's/\.txt/.xls/'`
cat ${OUT}.1 ${OUT}.2 ${OUT}.3 ${OUT}.4 > ${OUT}
/usr/local/package/python2.7/current/bin/python ${SCRIPT}/mkxls.py -i ${OUT} -x $OUT_XLS
/usr/local/package/python2.7/current/bin/python ${SCRIPT}/xl2tsv.py -t $OUT_TSV -x $OUT_XLS


: <<'#COMMENT'
#COMMENT

