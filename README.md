# GenomonPipeline
Genomon pipeline in 2015

## Dependency


## Install

```
git clone https://github.com/Genomon-Project/Genomon.git
cd Genomon
python setup.py build
python setup.py install --user
pip install xlrd --user
```

## Run
Disease sample vs. Control sample Comparison
```
genomon_summary [-h] {dna,rna} sample_conf.txt project_root_dir genomon_conf_file task_conf_file
```

For DNA sample

example.
```
genomon_summary dna ./sample_conf.txt ~/tmp ./genomon.cfg ./dna_task_param.cfg
```

For RNA sample

example.
```
genomon_summary rna ./sample_conf.txt ~/tmp ./genomon.cfg ./rna_task_param.cfg
```
