# -*- coding: utf-8 -*-
# Python Script for annotations via potato
# 
# Authors: Christian "Doofnase" Schuler, 
#          Deepesah "Tania" Saurty, 
#          Tramy Thi "Myy" Tran, 
#          Raman "Brudi" Ahmad, 
#          Anran "Echo" Wang
###############################################################################

""" Sources:
Potato: the POrtable Text Annotation TOol: https://github.com/davidjurgens/potato#potato-the-portable-text-annotation-tool
NLLB-Seed Machine Translation Data version 2: https://github.com/openlanguagedata/seed/blob/main/seed/eng_Latn
"""

""" User-Guide:
 0. Open a terminal and navigate to your desired directory:
cd PATH_TO_DIRECTORY/TextAsCorpusRep/experiments/annotation-potato
( cd /media/QereqolaXebate/CrazyProjects/DDLitLab-TextAsCorpusRep/TextAsCorpusRep/experiments/annotation-potato )

 1. Clone the github repository to your computer:
git clone git@github.com:davidjurgens/potato.git
( alternatively: git clone https://github.com/davidjurgens/potato.git )

 2. Prior to first start create a virtual environment named venvPotato via
python -m venv venvPotato
(you might have to use python3 instead of python)

 3. Then activate this environment via
source venvPotato/bin/activate

 4. Install the required python packages via
pip install -r ./potato/requirements.txt
(you might have to use pip3 instead of pip)

 5. To check installation, run a simple check-box style annotation on text data via
python potato/potato/flask_server.py start potato/project-hub/simple_examples/configs/simple-check-box.yaml -p 8000

This will launch the webserver on port 8000 which can be accessed via a webbrowser at 
http://localhost:8000
→ Username: doof@doof  → Password: 555nase

 6. Start our annotation experiment via
 6.1 Simple translation test
python potato/potato/flask_server.py start MTACR-december/MTACR-textbox.yaml -p 8000
 6.2 Translate 12 sentences
python potato/potato/flask_server.py start MTACR-annotation_suite/MTACR-12-trans.yaml -p 8000
 6.3 POS-Tag 12 sentences
python potato/potato/flask_server.py start MTACR-annotation_suite/MTACR-12-pos.yaml -p 8000

 → each of them should be found at:  http://localhost:8000

7. Use of this script to start potato via
python MTACR_potato.py -pa
python MTACR_potato.py -pt

 8. Highlight annotated text via
python MTACR_potato.py -hp \
    -ip /media/QereqolaXebate/CrazyProjects/DDLitLab-TextAsCorpusRep/TextAsCorpusRep/experiments/annotation-potato/MTACR-annotation_suite/annotation_output/MTACR-december-12-pos/christian@christian/annotated_instances.jsonl \
    -op /media/QereqolaXebate/CrazyProjects/DDLitLab-TextAsCorpusRep/TextAsCorpusRep/experiments/annotation-potato/MTACR-annotation_suite/output_images/ \
    -on deu_christian

 9. transform annotated text via
python MTACR_potato.py -ta \
    -ip /media/QereqolaXebate/CrazyProjects/DDLitLab-TextAsCorpusRep/TextAsCorpusRep/experiments/annotation-potato/MTACR-annotation_suite/annotation_output/MTACR-december-12-pos/christian@christian/annotated_instances.jsonl \
    -op /media/QereqolaXebate/CrazyProjects/DDLitLab-TextAsCorpusRep/TextAsCorpusRep/experiments/annotation-potato/MTACR-annotation_suite/output_transformed/ \
    -on deu_christian

 10. Plot previously highlighted annotated text via TODO: Requires to install-    pip intall matplotlib
python MTACR_potato.py -ph \
    -ip /media/QereqolaXebate/CrazyProjects/DDLitLab-TextAsCorpusRep/TextAsCorpusRep/experiments/annotation-potato/MTACR-annotation_suite/output_transformed/deu_christian.txt \
    -op /media/QereqolaXebate/CrazyProjects/DDLitLab-TextAsCorpusRep/TextAsCorpusRep/experiments/annotation-potato/MTACR-annotation_suite/output_images/ \
    -on deu_christian

"""
import annotate_potato_highlight
import annotate_potato_plot
import argparse
import logging
import os
import subprocess
import textwrap
import time
import transform_annotated_sentences
import webbrowser
"""

"""
def main(args, loglevel):
    logging.basicConfig(format="%(levelname)s: %(message)s", level=loglevel)
    logger = logging.getLogger('progress')

    # TODO Replace this with your actual code.
    # Get the start time
    start_time = time.time()

    
    # Process files from directory
    #input_text_files_path = args.inputPath[0]
    #output_json_files_path = args.outputPath[0]
    
    
    def run_example():
        pass

    """
    
    """
    def potato_annotating():
        command = "python potato/potato/flask_server.py start MTACR-annotation_suite/MTACR-12-pos.yaml -p 8000"
        subprocess.run(command, shell = True, executable="/bin/bash")
        # TODO: Have the server in the background and then open webbrowser automatically
        # webbrowser.open('http://localhost:8000', new=1)
        # If new is 0, the url is opened in the same browser window if possible. 
        # If new is 1, a new browser window is opened if possible. 
        # If new is 2, a new browser page (“tab”) is opened if possible
    """

    """
    def potato_translating():
        command = "python potato/potato/flask_server.py start MTACR-annotation_suite/MTACR-12-trans.yaml -p 8000"
        subprocess.run(command, shell = True, executable="/bin/bash")
        # TODO: Have the server in the background and then open webbrowser automatically
        # webbrowser.open('http://localhost:8000', new=1)

    """
    The method inside this script, called "highlight_pos_tags",
    calls another script, called "annotate_potato_highlight", which has been imported at the top.
    From this other script, the method "highlight_pos_tags_sentence" is called to do the highlighting.
    """
    def highlight_pos_tags():
        for i in range(len(args.inputPath)):
            annotate_potato_highlight.highlight_pos_tags_sentence(args.inputPath[i], args.outputPath[i], args.outputName[i])
    
    """
    
    """
    def transform_annotations():
        for i in range(len(args.inputPath)):
            transform_annotated_sentences.transform_annotations_for_plotting(args.inputPath[i], args.outputPath[i], args.outputName[i])

    """
    
    """
    def plot_highlighted_pos_tags():
        if args.example:
            example_case = True
        else:
            example_case = False
        for i in range(len(args.inputPath)):
            annotate_potato_plot.plot_highlighted_pos_tags_sentence(example_case, args.inputPath[i], args.outputPath[i], args.outputName[i])

    # Take the input arguments to then decide which mode to run
    def mode_script():
        if args.example:
            logging.info("Run example:")
            run_example()
        elif args.potatoAnnotate:
            logging.info("Run potato for annotation task:")
            potato_annotating()
        elif args.potatoTranslate:
            logging.info("Run potato for translation task:")
            potato_translating()
        elif args.highlightPos:
            logging.info("Run highlight of pos-tags:")
            highlight_pos_tags()
        elif args.transformAnnotations:
            logging.info("Run transformation of annotated data:")
            transform_annotations()
        elif args.plotHighlight:
            logging.info("Run plot of highlighted sentences:")
            plot_highlighted_pos_tags()
        else:
            logging.info("No argument for execution mode provided.")

    mode_script()

    end_time = time.time()
    execution_time = end_time - start_time
    execution_time_minutes = round((execution_time / 60), 3)
    logging.info('Execution time: '+str(execution_time_minutes)+' minutes')

    logging.info("Info: End of script.")


# Standard boilerplate to call the main() function to begin the program.
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        #prog='PROG',
        #description=__doc__,
        description=textwrap.dedent('''\
            Description of Script/Module
            ---------------------------------------------
            For more information check out the github repository:
            https://github.com/Low-ResourceDialectology/TextAsCorpusRep
            '''),
        epilog = "As an alternative to the commandline, params can be placed in a file, one per line, and specified on the commandline like '%(prog)s @params.conf'.",
        fromfile_prefix_chars = '@' )
        # Specify your real parameters here:
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="increase output verbosity.")
    parser.add_argument(
        '-e', '--example', 
        action="store_true", 
        help='example run for testing.')
    parser.add_argument(
        '-ip', '--inputPath', 
        nargs="+", 
        type=str,
        help='path to input files.')
    parser.add_argument(
        '-op', '--outputPath', 
        nargs="+", 
        type=str,
        help='path to output files.')
    parser.add_argument(
        '-on', '--outputName', 
        nargs="+", 
        type=str,
        help='name of output files.')
    parser.add_argument(
        '-hp', '--highlightPos', 
        action="store_true", 
        help='highlight POS-Tags in text sentences.')
    parser.add_argument(
        '-ph', '--plotHighlight', 
        action="store_true", 
        help='plot text sentences with their POS-Tags highlighted.')
    parser.add_argument(
        '-ta', '--transformAnnotations', 
        action="store_true", 
        help='transform the annotations for easy plotting of the highlighted tags.')
    parser.add_argument(
        '-pt', '--potatoTranslate', 
        action="store_true", 
        help='start potato to translate sentences.')
    parser.add_argument(
        '-pa', '--potatoAnnotate', 
        action="store_true", 
        help='start potato to annotate sentences.')
    
    args = parser.parse_args()
    
    # Setup logging
    if args.verbose:
        loglevel = logging.DEBUG
    else:
        loglevel = logging.INFO
    
    main(args, loglevel)