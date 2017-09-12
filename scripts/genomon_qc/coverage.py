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
# create -i BED, for bedtools shuffle
#
def create_i_bed_wgs(output_bed, line_num, width):
    f = open(output_bed, "w")
    for i in range(line_num):
        f.write("1\t0\t%d\n" % (width))

    f.close()
    
#
# Calculate coverage
#
def calc_coverage(depth_file, bed_file, coverage_depth, output):
    import os
    import pandas
    import math

    if not os.path.exists(bed_file):
        print "Not exist file, " + bed_file
        return
        
    bed = pandas.read_csv(bed_file, header = None, sep='\t', usecols = [1,2])
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
set -o pipefail

export LD_LIBRARY_PATH={LD_LIBRARY_PATH}

# for hg19, create gap text (bedtools shuffle -excl option file)
cut -f 2,3,4 {gaptxt} && cut -c 4- > {output}.shuffle_excl.bed

# bedtools shuffle
{BEDTOOLS} shuffle -i {i_bed_file} -g {genome_size_file} -incl {incl_bed_file} -excl {output}.shuffle_excl.bed > {output}.target.bed

# depth
if [ -e {output}.tmp ]; then
    rm {output}.tmp || exit $?
fi

cat {output}.target.bed | while read line; do (
    set -- $line || exit $?
    let start=$2+1 || exit $?
    
    {SAMTOOLS} view {samtools_params} -b -h {input} $1:$start-$3 > {output}.tmp.bam
    {SAMTOOLS} index {output}.tmp.bam || exit $?
    {SAMTOOLS} depth -r $1:$start-$3 {output}.tmp.bam >> {output}.tmp

) </dev/null; done

mv {output}.tmp {output}
"""
    output_prefix = os.path.dirname(args.output_file)
    create_incl_bed_wgs(args.genome_size_file, output_prefix + '/depth.shuffle_incl.bed', args.incl_bed_width, "")
    create_i_bed_wgs(output_prefix + '/depth.shuffle_i.bed', args.i_bed_lines, args.i_bed_width)
    cmd = cmd_template.format(input = args.input_file,
                            output = output_prefix + '/depth',
                            gaptxt = args.gaptxt,
                            #i_bed_lines = args.i_bed_lines,
                            #i_bed_width = args.i_bed_width,
                            genome_size_file = args.genome_size_file,
                            incl_bed_file = output_prefix + '/depth.shuffle_incl.bed',
                            i_bed_file = output_prefix + '/depth.shuffle_i.bed',
                            LD_LIBRARY_PATH = args.ld_library_path,
                            BEDTOOLS = args.bedtools,
                            SAMTOOLS = args.samtools,
                            samtools_params = args.samtools_params)

    subprocess.check_call(cmd, shell=True)
    calc_coverage(output_prefix + '/depth', output_prefix + '/depth.target.bed', args.coverage_text, args.output_file)

    if args.del_tempfile == True:
        os.unlink(output_prefix + '/depth.shuffle_i.bed')
        os.unlink(output_prefix + '/depth.shuffle_incl.bed')
        os.unlink(output_prefix + '/depth.shuffle_excl.bed')
        os.unlink(output_prefix + '/depth.target.bed')
        os.unlink(output_prefix + '/depth.tmp.bam')
        os.unlink(output_prefix + '/depth.tmp.bam.bai')
        os.unlink(output_prefix + '/depth')
        

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
set -o pipefail

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
    
    output_prefix = os.path.dirname(args.output_file)
    cmd = cmd_template.format(input = args.input_file,
                            output = output_prefix + '/depth',
                            bait_file = args.bait_file,
                            LD_LIBRARY_PATH = args.ld_library_path,
                            BEDTOOLS = args.bedtools,
                            SAMTOOLS = args.samtools,
                            samtools_params = args.samtools_params,
                            )

    subprocess.check_call(cmd, shell=True)
    calc_coverage(output_prefix + '/depth', output_prefix + '/depth.target.bed', args.coverage_text, args.output_file)
    
    if args.del_tempfile == True:
        os.unlink(output_prefix + '/depth.target.bed')
        os.unlink(output_prefix + '/depth.noheader.bed')
        os.unlink(output_prefix + '/depth.sort.bed')
        os.unlink(output_prefix + '/depth.merge.bed')
        os.unlink(output_prefix + '/depth')


if __name__ == "__main__":
    pass


    
