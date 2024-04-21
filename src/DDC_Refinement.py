import csv
import functools
import os
import time

from src import String_Comparator

save_to_file = False
save_to_file_path = 'intermediary/DDC_Refinement.csv'
statistics_path = 'intermediary/DDC_Refinement_Statistics.csv'


def generate_operand_to_ddcs(refined_ddcs, data, ddcs, refine_method, special_characters_flag, camel_case_flag,
                             threshold):
    operand_to_ddcs = {}
    operands = " ".join(data[2].split()).split(",")

    for operand in operands:
        start_time = time.time()
        generate_temp_ddc_for_operand(data, ddcs, operand.strip(), operand_to_ddcs, refine_method,
                                      special_characters_flag, camel_case_flag, threshold)
        print("--- Generated operand: ", operand.strip(), ", DDCs: ", len(operand_to_ddcs[operand.strip()]), ", in %s seconds ---" % (time.time() - start_time))

    refined_ddcs[data[0]] = operand_to_ddcs


def generate_operand_to_tokens(refined_ddcs, data, ddcs, refine_method, special_characters_flag, camel_case_flag,
                             threshold):
    operand_to_ddcs = {}
    operands = " ".join(data[2].split()).split(",")

    for operand in operands:
        start_time = time.time()
        generate_temp_tokens_for_operand(data, ddcs, operand.strip(), operand_to_ddcs, refine_method,
                                      special_characters_flag, camel_case_flag, threshold)
        print("--- Generated operand: ", operand.strip(), ", DDCs: ", len(operand_to_ddcs[operand.strip()]), ", in %s seconds ---" % (time.time() - start_time))

    refined_ddcs[data[0]] = operand_to_ddcs


def generate_temp_ddc_for_operand(data, ddcs, operand, operand_to_ddcs, refine_method,
                                  special_characters_flag, camel_case_flag, threshold):
    temp_ddc = []
    # filter after the system
    for ddc in [e for e in ddcs if e[0] == data[1]]:
        # for each operand we have list of possible DDCs
        if String_Comparator.check_similarity_ddc_operand(ddc, operand, refine_method, threshold, special_characters_flag, camel_case_flag):
            temp_ddc.append(ddc)
    operand_to_ddcs[operand] = temp_ddc


def generate_temp_tokens_for_operand(data, ddcs, operand, operand_to_ddcs, refine_method,
                                  special_characters_flag, camel_case_flag, threshold):
    temp_ddc = []
    # filter after the system
    for ddc in [e for e in ddcs if e[0] == data[1]]:
        # for each operand we have list of possible DDCs
        String_Comparator.get_tokens_ddc_operand(ddc, operand, temp_ddc, refine_method, threshold,
                                                 special_characters_flag, camel_case_flag)
    operand_to_ddcs[operand] = temp_ddc


def refine_ddc(constraints, ddcs, refine_method, threshold, special_characters_flag, camel_case_flag):
    # DDP refinement: process the extracted DDP using the constraints operands

    refined_ddcs = {}
    for data in constraints:
        generate_operand_to_ddcs(refined_ddcs, data, ddcs, refine_method, special_characters_flag, camel_case_flag,
                                 threshold)
    return refined_ddcs


def refine_tokens(constraints, ddcs, refine_method, threshold, special_characters_flag, camel_case_flag):
    # DDP refinement: process the extracted DDP using the constraints operands

    refined_ddcs = {}
    for data in constraints:
        generate_operand_to_tokens(refined_ddcs, data, ddcs, refine_method, special_characters_flag, camel_case_flag,
                                 threshold)
    return refined_ddcs


def refine_multi_process(constraints, ddcs, refine_method, threshold, tokenize_option, special_characters_flag,
                         language, multi_pocess):
    # DDP refinement: process the extracted DDP using the constraints operands

    from multiprocessing import Manager, Pool

    manager = Manager()
    refined_ddcs = manager.dict()

    def generate_operand_to_ddcs2(data, ddcs, language, refine_method, special_characters_flag, threshold,
                                  tokenize_option):
        start_time = time.time()
        operand_to_ddcs = {}
        operands = " ".join(data[2].lower().split()).split(",")

        for operand in operands:
            generate_temp_ddc_for_operand(data, ddcs, language, operand.strip(), operand_to_ddcs, refine_method,
                                          special_characters_flag, threshold, tokenize_option)

        print("--- Generated operand to ddcs for one constraint in %s seconds ---" % (time.time() - start_time))

        refined_ddcs[data[0]] = operand_to_ddcs

    pool = Pool(processes=multi_pocess)
    pool.imap(functools.partial(generate_operand_to_ddcs2, 2, optional_param=3), [1, 2, 3, 4, 5])

    pool.map(generate_operand_to_ddcs, args=(constraints, ddcs, language, refine_method, special_characters_flag,
                                             threshold,
                                             tokenize_option))
    pool.close()

    # refined_ddcs = {}
    # for data in constraints:
    #     generate_operand_to_ddcs(refined_ddcs, data, ddcs, language, refine_method, special_characters_flag,
    #                              threshold,
    #                              tokenize_option)
    return refined_ddcs


def save_to_file():
    save_to_file = True


def remove_file():
    save_to_file = False
    os.remove(save_to_file_path)


def print_ddc(dict):
    print('-------------------')
    for key, value in dict.items():
        print(len(value), ':', key)
    print('-------------------')


def get_statistics(ddcs, constraints, refine_method):
    header = ['constraint', 'operand', '# of results', 'matched ? 1/0']

    statistics_path_refined = statistics_path.split(".")[0] + '_refine' + refine_method.__str__() + "." + \
                              statistics_path.split(".")[1]

    # open the file in the write mode
    with open(statistics_path_refined, 'w') as f:
        writer = csv.writer(f)
        # write the header
        writer.writerow(header)

        for constraint in constraints:
            if constraint[1]:
                operand, path = constraint[1].split(",", 1)
                operand = operand.strip()
                if operand not in ddcs[constraint[0]].keys():
                    print(constraint[0], ",", operand)
                else:
                    matched1 = 0
                    for ddc in ddcs[constraint[0]][operand]:
                        if ddc[2] in path and ddc[3].split(":")[0] in path:
                            matched1 = 1
                    # write the data
                    writer.writerow([constraint[0], operand, len(ddcs[constraint[0]][operand]), matched1])

            if constraint[2]:
                operand, path = constraint[2].split(",", 1)
                operand = operand.strip()
                if operand not in ddcs[constraint[0]].keys():
                    print(constraint[0], ",", operand)
                else:
                    matched2 = 0
                    for ddc in ddcs[constraint[0]][operand]:
                        if 'compositeCount' in ddc[6] and 'composite instance' in operand:
                            print('aaa')
                        if ddc[2] in path and ddc[3].split(":")[0] in path:
                            matched2 = 1
                    # write the data
                    writer.writerow([constraint[0], operand, len(ddcs[constraint[0]][operand]), matched2])