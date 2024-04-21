import argparse

from src import Controller

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--folder', default='input/data', help='path to the system data folder.')
parser.add_argument('-i', '--input', default='input/input_constraints_datadefinitions.csv',
                    help='Path to the '
                         'constraints '
                         'document.')

parser.add_argument('-o', '--option', default=0,
                    help='Options for the program:'
                         '\n 0.Links'
                         '\n 1.DDC'
                         '\n 2.ESC')

parser.add_argument('-s', '--save', default=True,
                    help='Flag for saving and using the extracted query data to file.')

parser.add_argument('-r', '--refine', default=1,
                    help='Refine method applied between the java code and constraint '
                         'operands. \n 0-Equal \n 1-Contains \n 2-Contains + Class')

parser.add_argument('-t', '--threshold', default=0.65,
                    help='The float value above which elements should be accepted for the refinement method.')

parser.add_argument('-sc', '--special_characters',  #default=True,
                    help='The code tokenizer option to split the tokens from the code by special(non aplha-numeric) '
                         'characters.')

parser.add_argument('-cc', '--camel_case',  default=True,
                    help='The code tokenizer option to split the tokens from the code by camel-case.')

args = parser.parse_args()

Controller.main(args.folder, args.input, args.option, args.save is not None, args.refine, args.threshold,
                args.special_characters is not None, args.camel_case is not None)
