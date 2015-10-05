#! /usr/bin/env python

from ruffus import *
from genomon_summary.config.genomon_conf import *
from genomon_summary.config.task_conf import *
from genomon_summary.config.run_conf import *
from genomon_summary.config.sample_conf import *

def main(args):

    ###
    # set run_conf
    run_conf.sample_conf_file = args.sample_list_file
    run_conf.analysis_type = args.analysis_type
    run_conf.project_root = args.project_root
    run_conf.genomon_conf_file = args.genomon_conf_file
    run_conf.task_conf_file = args.task_conf_file
    ###

    ###
    # read sample list file
    sample_conf.parse_file(run_conf.sample_conf_file)
    ###

    ###
    # set and check genomon_conf config data
    genomon_conf.read(run_conf.genomon_conf_file)
    genomon_conf_check()
    ###

    ###
    # set and check task parameter config data    
    task_conf.read(run_conf.task_conf_file)
    task_conf_check()
    ###
    
    import pipeline
    pipeline_run(verbose = 3, multiprocess = 200)

    """
    pipeline_printout_graph (
        open("/home/okada/genomon_summary.svg", "w"),
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
        pipeline_name = "Genomon Summary Schemes"
     )
    """
