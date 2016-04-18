# GenomonQC
Genomon Quality Control in 2015

## Dependency

 - python 2.7
 - ruffus 2.6.3

## Install

```
git clone https://github.com/Genomon-Project/GenomonQC.git
cd Genomon
python setup.py build
python setup.py install --user
```

## Run
Disease sample vs. Control sample Comparison
```
genomon_qc [-h] {wgs,exome} sample_conf_file project_root_dir conf_file
```

For WGS sample

example.
```
genomon_qc wgs ./sample_conf.txt ~/tmp ./genomon.cfg
```

For EXOME sample

example.
```
genomon_qc exome ./sample_conf.txt ~/tmp ./genomon.cfg
```
