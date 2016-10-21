# -*- coding: utf-8 -*-
"""
Created on Thu Oct 20 13:59:56 2016

@author: okada
"""

# 
# create -incl BED, for bedtools shuffle
#
def create_incl_bed_wgs(input_genome, output_bed, width, suffix):
    import os
    import math
   
    if not os.path.exists(input_genome):
        print "Not exist file, " + input_genome
        return

    # read genome file to dict.
    genomes = {}
    for line in open(input_genome):
        cells = line.rstrip().split("\t")
        if len(cells) < 2:
            break
        chrom = cells[0].lower().replace("chr", "")
    
        if chrom.isdigit() == True or chrom == "x" or chrom == "y":
            genomes[chrom] = long(cells[1])
    
    # write BED file
    f = open(output_bed, "w") 
    for key in genomes:

        size = genomes[key]
        start = 0
        end = width

        line_num = long(math.ceil(float(size)/float(width)))
        for j in range(line_num):
            if end > size:
                end = size

            head = suffix + key.upper()

            f.write("{0}\t{1}\t{2}\n".format(head, start, end))
            start = end
            end += width

    f.close()
    
#
# Calculate coverage
#
def calc_coverage(depth_file, coverage_depth, output):
    import pandas
    import math

    if not os.path.exists(depth_file + ".input_bed"):
        print "Not exist file, " + depth_file + ".input_bed"
        return
        
    bed = pandas.read_csv(depth_file + ".input_bed", header = None, sep='\t', usecols = [1,2])
    all_count = sum(bed[2] - bed[1])

    # depth average & coverage
    depth_reader = pandas.read_csv(depth_file, header = None, sep='\t', usecols = [2], chunksize = 10000)
    
    all_sum = 0
    coverage = {}
    for depth in depth_reader:
        all_sum += sum(depth[2])
        
        for num in coverage_depth.split(','):
            filt = depth[(depth[2] >= int(num))]
            if (num in coverage) == True:
                count = coverage[num][0] + len(filt)
            else:
                count = len(filt)

            coverage[num] = [count, 0]
    
    for num in coverage_depth.split(','):
        ratio = float(coverage[num][0])/float(all_count)
        coverage[num] = [coverage[num][0], ratio]
            
    ave = float(all_sum)/float(all_count)
    
    # depth std
    depth_reader = pandas.read_csv(depth_file, header = None, sep='\t', usecols = [2], dtype = 'float', chunksize = 10000)
    dist2 = 0
    for depth in depth_reader:
        dist2 += sum((depth[2] - ave)**2)
    
    std = math.sqrt(dist2/float(all_count))

    #
    # Output result
    #
    header_string =  "total_depth\tbait_size\taverage_depth\tdepth_stdev"
    data_string = "{0}\t{1}\t{2}\t{3}".format(all_sum, all_count, ave, std)
    
    num_header_string = ""
    ratio_header_string = ""
    num_string = ""
    ratio_string = ""
    
    for num in coverage_depth.split(','):
    
        num_header_string += "\t{0}x".format(num)
        ratio_header_string += "\t{0}x_ratio".format(num)
        num_string += "\t{0}".format(coverage[num][0])
        ratio_string += "\t{0}".format(coverage[num][1])
        
    header_string += ratio_header_string + num_header_string
    data_string += ratio_string + num_string
    
    f = open(output, "w")
    f.write(header_string)
    f.write('\n')
    f.write(data_string)
    f.close()
    
# 
# run wgs
#
def run_wgs(args):
    
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
set -eu

export LD_LIBRARY_PATH={LD_LIBRARY_PATH}

# for hg19, create gap text (bedtools shuffle -excl option file)
cut -f 2,3,4 {gaptxt} | cut -c 4- > {output}.gap.txt

# create temp bed (bedtools shuffle -i option file)
echo '' > {output}.shuffle.bed
for J in `seq 1 {i_bed_lines}`
do
    printf "1\t0\t%s\n" {i_bed_width} >> {output}.shuffle.bed
done

# bedtools shuffle
{BEDTOOLS} shuffle -i {output}.shuffle.bed -g {genome_size_file} -incl {incl_bed_file} -excl {output}.gap.txt > {output}.target.bed

# depth
if [ -e {output}.tmp ]; then
    rm {output}.tmp
fi

cat {output}.target.bed | while read line; do (
    set -- $line
    let start=$2+1
    
    {SAMTOOLS} view {samtools_params} -b -h {input} $1:$start-$3 > {output}.tmp.bam
    {SAMTOOLS} index {output}.tmp.bam
    {SAMTOOLS} depth -r $1:$start-$3 {output}.tmp.bam >> {output}.tmp

) </dev/null; done

mv {output}.tmp {output}
"""

    create_incl_bed_wgs(args.genome_size_file, args.output_prefix + '.incl.bed', args.incl_bed_width, "")

    cmd = cmd_template.format(input = args.input_file,
                            output = args.output_prefix + '.depth',
                            gaptxt = args.gaptxt,
                            i_bed_lines = args.i_bed_lines,
                            i_bed_width = args.i_bed_width,
                            genome_size_file = args.genome_size_file,
                            incl_bed_file = args.output_prefix + '.incl.bed',
                            LD_LIBRARY_PATH = args.ld_library_path,
                            BEDTOOLS = args.bedtools,
                            SAMTOOLS = args.samtools,
                            samtools_params = args.samtools_params)

    subprocess.check_call(cmd, shell=True)
    calc_coverage(args.output_prefix + '.depth', args.coverage_text, args.output_prefix + '.coverage')

    if args.del_tempfile == True:
        os.unlink(args.output_prefix + '.shuffle.bed')
        os.unlink(args.output_prefix + '.incl.bed')
        os.unlink(args.output_prefix + '.gap.txt')
        os.unlink(args.output_prefix + '.target.bed')
        os.unlink(args.output_prefix + '.tmp.bam')
        os.unlink(args.output_prefix + '.tmp.bam.bai')
        os.unlink(args.output_prefix + '.depth')
        

# 
# run exome
#
def run_exome(args):
    
    import os
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
set -eu

export LD_LIBRARY_PATH={LD_LIBRARY_PATH}

    # merge bed (bedtools shuffle -incl option file)
    total_l=`cat {bait_file} | wc -l`
    header_l=`grep ^@ {bait_file} | wc -l`
    data_l=`expr $total_l - $header_l`
    tail -$data_l {bait_file} > {output}.noheader.bed
    {BEDTOOLS} sort -i {output}.noheader.bed > {output}.sort.bed
    {BEDTOOLS} merge -i {output}.sort.bed > {output}.merge.bed
    cut -c 4- {output}.merge.bed > {output}.target.bed

    # depth
    {SAMTOOLS} view {samtools_params} -b -h {input} | {SAMTOOLS} depth -b {output}.target.bed - > {output}.tmp

mv {output}.tmp {output}
"""
    
    cmd = cmd_template.format(input = args.input_file,
                            output = args.output_prefix + '.depth',
                            bait_file = args.bait_file,
                            LD_LIBRARY_PATH = args.ld_library_path,
                            BEDTOOLS = args.bedtools,
                            SAMTOOLS = args.samtools,
                            samtools_params = args.samtools_params,
                            )

    subprocess.check_call(cmd, shell=True)
    calc_coverage(args.output_prefix + '.depth', args.coverage_text, args.output_prefix + '.coverage')
    
    if args.del_tempfile == True:
        os.unlink(args.output_prefix + '.target.bed')
        os.unlink(args.output_prefix + '.noheader.bed')
        os.unlink(args.output_prefix + '.sort.bed')
        os.unlink(args.output_prefix + '.merge.bed')
        os.unlink(args.output_prefix + '.depth')


if __name__ == "__main__":
    pass


    
