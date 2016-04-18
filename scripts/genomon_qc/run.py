#! /usr/bin/env python

from ruffus import *
from genomon_qc.config.genomon_conf import *
from genomon_qc.config.run_conf import *
from genomon_qc.config.sample_conf import *

def main(args):

    ###
    # set run_conf
    run_conf.sample_conf_file = args.sample_conf_file
    run_conf.analysis_type = args.analysis_type
    run_conf.project_root = os.path.abspath(args.project_root)
    run_conf.genomon_conf_file = args.genomon_conf_file

    ###
    # read sample list file
    sample_conf.parse_file(run_conf.sample_conf_file)

    ###
    # set genomon_conf and task parameter config data
    genomon_conf.read(run_conf.genomon_conf_file)
    dna_genomon_conf_check()
    #dna_software_version_set()
    import pipeline
    
    pipeline_run(
        verbose = args.verbose, 
        multiprocess = args.multiprocess
        )

    """
    pipeline_printout_graph (
        open("/home/okada/genomon_qc.svg", "w"),
        "svg",
        # final targets
        [pipeline.merge],
        # Explicitly specified tasks
#        [dna_pipeline.link_input_fastq],
        draw_vertically = False,
        test_all_task_for_update = True,
        user_colour_scheme = {
            "colour_scheme_index" :0,
        },
        pipeline_name = "Genomon QC Schemes"
     )
    """
