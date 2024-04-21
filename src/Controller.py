import csv
import sys

import ESC_Extraction
from src import DDC_Refinement, DDC_Extraction, ESC_Refinement


def main(folder, master_document, run_option, saved_option, refine_method, threshold, special_characters_flag, camel_case_flag):
    if run_option == 0:
        print_run_option(run_option)

        # read the input constraints data
        data_read = read_constraints(master_document)

        # extract the DDC
        ddc = extract_DDC(data_read, folder, saved_option)

        # extract the ESC
        esc = extract_ESC(data_read, folder, saved_option)

        # refining DDC to Constraint operands
        print('Refining extracted DDCs with technique ' + str(refine_method) + '...')
        DDC_Refinement.save_to_file()
        constraint_to_operand_to_ddc = DDC_Refinement.refine_tokens([[el[0], el[2], el[12]] for el in data_read], ddc, refine_method, threshold, special_characters_flag, camel_case_flag)
        print('Refined', len(constraint_to_operand_to_ddc), 'constraints', sum([len(y) for y in constraint_to_operand_to_ddc.values()]), 'operands')

        # refining ESC to constraint
        print('Refining extracted ESCs with technique ' + str(refine_method) + '...')
        ESC_Refinement.save_to_file()
        constraint_to_esc = ESC_Refinement.refine({el[0]: el[2] for el in data_read}, constraint_to_operand_to_ddc, esc, special_characters_flag, camel_case_flag)
        print('Refined', len(constraint_to_esc), 'constraints')
        ESC_Refinement.get_statistics(constraint_to_esc, [[el[0], el[16]] for el in data_read], refine_method)

        # rank ESCs
        # TODO

    elif run_option == 1:
        print_run_option(run_option)

        # read the input constraints data
        data_read = read_constraints(master_document)

        # extract the DDC
        ddc = extract_DDC(data_read, folder, saved_option)

        # refining DDC to Constraint operands
        print('Refining extracted DDCs with technique ' + str(refine_method) + '...')
        DDC_Refinement.save_to_file()
        constraint_to_operand_to_ddc = DDC_Refinement.refine_ddc([[el[0], el[2], el[12]] for el in data_read], ddc,
                                                                 refine_method, threshold, special_characters_flag,
                                                                 camel_case_flag)
        print('Refined', len(constraint_to_operand_to_ddc), 'constraints',
              sum([len(y) for y in constraint_to_operand_to_ddc.values()]), 'operands')
        # DDC_Refinement.print_ddc(constraint_to_ddc)
        DDC_Refinement.get_statistics(constraint_to_operand_to_ddc, [[el[0], el[18], el[19]] for el in data_read],
                                      refine_method)

    elif run_option == 2:
        print_run_option(run_option)

        # read the input constraints data
        data_read = read_constraints(master_document)

        # extract the ESC
        esc = extract_ESC(data_read, folder, False)

    else:
        print('Wrong Option!')


def print_run_option(run_option):
    options = {
        0 : 'Running Constraint-ESC Link',
        1 : 'Running DDC extraction and refinement',
        2 : 'Running ESC extraction'
    }
    print('-------------------')
    print(options[run_option])
    print('-------------------')
    print()


def extract_ESC(data_read, folder, saved_option):
    print('Extracting ESCs...')
    esc = ESC_Extraction.extract(folder, saved_option)
    print('Extracted ', len(esc), ' ESCs')
    ESC_Extraction.print_esc(esc)
    # todo eliminate the last el because it was used to debug not matched constraints
    ESC_Extraction.get_statistics(esc, [[el[0], el[2], el[16], el[17], el[24]] for el in data_read])
    return esc


def extract_DDC(data_read, folder, saved_option):
    print('Extracting DDCs...')
    ddc = DDC_Extraction.extract(folder, saved_option)
    print('Extracted ', len(ddc), ' DDCs')
    DDC_Extraction.print_ddc(ddc)
    DDC_Extraction.get_statistics(ddc, [[el[0], el[2], el[18], el[19], el[26], el[28]] for el in data_read])
    return ddc


def read_constraints(master_document):
    with open(master_document) as fp:
        reader = csv.reader(fp, delimiter=",", quotechar='"')
        next(reader, None)  # skip the headers
        data_read = [row for row in reader]
    print('Read', len(data_read), 'constraints')
    print()
    return data_read


if __name__ == '__main__':
    main(sys.args)