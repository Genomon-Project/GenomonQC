# GenomonQC
Genomon Quality Control in 2015

## Dependency

 - python (2.7.x)
 - samtools (1.2)
 - bedtools (2.24.0)
 - PCAP (20150511)

## Install

```
git clone https://github.com/Genomon-Project/GenomonQC.git
cd Genomon
python setup.py build
python setup.py install --user
vi genomon_qc.cfg
(write path to installed tools)
```

## Run

Disease sample vs. Control sample Comparison

### 1. For WGS sample

```
# calc coverage
genomon_qc wgs /path/to/sample.bam /path/to/output.coverage.txt --config_file /path/to/genomon_qc.cfg
# => output /path/to/output.coverage.txt

# bamstats
genomon_qc bamstats /path/to/sample.bam /path/to/output.bamstats.txt --config_file /path/to/genomon_qc.cfg
# => output /path/to/output.bamstats.txt

# merge output 2 files
genomon_qc merge /path/to/output.coverage.txt /path/to/output.merge.csv --config_file /path/to/genomon_qc.cfg
# => output /path/to/output.merge.csv
```

### 2. For EXOME sample

```
# calc coverage
genomon_qc exome /path/to/sample.bam /path/to/output.coverage.txt --config_file /path/to/genomon_qc.cfg
# => output /path/to/output.coverage.txt

# bamstats
genomon_qc bamstats /path/to/sample.bam /path/to/output.bamstats.txt --config_file /path/to/genomon_qc.cfg
# => output /path/to/output.bamstats.txt

# merge output 2 files
genomon_qc merge /path/to/output.coverage.txt /path/to/output.merge.csv --config_file /path/to/genomon_qc.cfg
# => output /path/to/output.merge.csv
```


## command

```
$ genomon_qc -h
usage: genomon_qc
[-h]
[--version] {wgs,exome,bamstats,merge} ...

positional arguments:
  {wgs,exome,bamstats,merge}
    wgs                 calc coverage for wgs.
    exome               calc coverage for exome.
    bamstats            bamstat.
    merge               merge coverage and bamstat.

optional arguments:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
```

### 1. calc coverage (wgs)

```
$ genomon_qc wgs -h
usage: genomon_qc wgs [-h]
                      [--genome_size_file GENOME_SIZE_FILE] 
                      [--gaptxt GAPTXT] 
                      [--incl_bed_width INCL_BED_WIDTH] 
                      [--i_bed_lines I_BED_LINES] 
                      [--i_bed_width I_BED_WIDTH]
                      [--ld_library_path LD_LIBRARY_PATH] 
                      [--bedtools BEDTOOLS] 
                      [--samtools SAMTOOLS] 
                      [--samtools_params SAMTOOLS_PARAMS] 
                      [--coverage_text COVERAGE_TEXT]
                      [--del_tempfile DEL_TEMPFILE] 
                      [--config_file CONFIG_FILE]
                      input_file output_file

positional arguments:
  input_file            path to input bam
  output_file           path to output file

optional arguments:
  -h, --help            show this help message and exit
  --genome_size_file GENOME_SIZE_FILE
                        path to the bedtools-2.24.0/genomes/human.hg19.genome
  --gaptxt GAPTXT       path to the gat.txt
  --incl_bed_width INCL_BED_WIDTH
                        bps for normalize incl_bed (bedtools chuffle -incl)
  --i_bed_lines I_BED_LINES
                        line number of target bed file.
  --i_bed_width I_BED_WIDTH
                        bps par 1 line, number of target bed file.
  --ld_library_path LD_LIBRARY_PATH
                        LD_LIBRARY_PATH
  --bedtools BEDTOOLS   path to installed BEDTOOLS
  --samtools SAMTOOLS   path to installed SAMTOOLS
  --samtools_params SAMTOOLS_PARAMS
                        SAMTOOL's parameters
  --coverage_text COVERAGE_TEXT
                        coverage_depth text separated with comma
  --config_file CONFIG_FILE
                        path to config file. use this file insead of specify above optional arguments.
  --del_tempfile DEL_TEMPFILE
                        delete flg to temporary file
```

### 2. calc coverage (exome)

```
$ genomon_qc exome -h
usage: genomon_qc exome [-h]
                        [--bait_file BAIT_FILE]
                        [--ld_library_path LD_LIBRARY_PATH]
                        [--bedtools BEDTOOLS]
                        [--samtools SAMTOOLS]
                        [--samtools_params SAMTOOLS_PARAMS]
                        [--coverage_text COVERAGE_TEXT]
                        [--del_tempfile DEL_TEMPFILE]
                        [--config_file CONFIG_FILE]
                        input_file output_file

positional arguments:
  input_file            path to input bam
  output_file           path to output file

optional arguments:
  -h, --help            show this help message and exit
  --bait_file BAIT_FILE
                        path to the bait_file
  --ld_library_path LD_LIBRARY_PATH
                        LD_LIBRARY_PATH
  --bedtools BEDTOOLS   path to installed BEDTOOLS
  --samtools SAMTOOLS   path to installed SAMTOOLS
  --samtools_params SAMTOOLS_PARAMS
                        SAMTOOL's parameters
  --coverage_text COVERAGE_TEXT
                        coverage_depth text separated with comma
  --config_file CONFIG_FILE
                        path to config file. use this file insead of specify above optional arguments.
  --del_tempfile DEL_TEMPFILE
                        delete flg to temporary file
```

### 3. bam_stats

```
$ genomon_qc bamstats -h
usage: genomon_qc bamstats [-h]
                           [--perl5lib PERL5LIB]
                           [--bamstats BAMSTATS]
                           [--config_file CONFIG_FILE]
                           input_file output_file

positional arguments:
  input_file            path to input bam
  output_file           path to output file

optional arguments:
  -h, --help            show this help message and exit
  --perl5lib PERL5LIB   PERL5LIB
  --bamstats BAMSTATS   installed file path of bamstats
  --config_file CONFIG_FILE
                        path to config file. use this file insead of specify above optional arguments.
```

### 4. merge file

```
$ genomon_qc merge -h
usage: genomon_qc merge [-h] 
                        [--meta META] 
                        [--config_file CONFIG_FILE] 
                        coverage_file bamstats_file output_file

positional arguments:
  coverage_file         path to coverage result file, created by wgs or exome.
  bamstats_file         path to bamstats result file, created by bamstats.
  output_file           path to output file.

optional arguments:
  -h, --help            show this help message and exit
  --config_file CONFIG_FILE
                        path to config file. use this file insead of specify above optional arguments.
  --meta META           meta data
  
```

