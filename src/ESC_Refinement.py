import csv
import os
import time

from src import String_Comparator

save_to_file = False
save_to_file_path = 'intermediary/ESC_Refinement.csv'
statistics_path = 'intermediary/ESC_Refinement_Statistics.csv'

UNIMPLEMENTED_OPERANDS = ['true', 'selected', 'specified', 'present', 'false', 'provided', 'on', 'set']
UNIMPLEMENTED_OPERANDS_2 = ['true', 'selected', 'specified', 'present', 'false', 'provided', 'on', 'set',
                          'empty', 'enabled', 'given', 'found', 'not set', 'supplied', 'not found',
                          'encoding considerations', 'omitted', 'used', 'not specified', 'checked']
UNIMPLEMENTED_OPERANDS_3 = ['true', 'selected', 'specified', 'present', 'false', 'provided', 'on', 'set',
                          'empty', 'enabled', 'given', 'found', 'not set', 'supplied', 'not found',
                          'encoding considerations', 'omitted', 'used', 'not specified', 'checked',
                          'available', 'negative', 'unrecognized', 'unknown', 'zero', 'not existing',
                          '16348', 'unique ids', 'persistent', 'disabled', 'active', 'not defined',
                          'positive', 'not given', 'namespace', 'not exist', 'off', 'identity',
                          'log level']













def save_to_file():
    save_to_file = True


def remove_file():
    save_to_file = False
    os.remove(save_to_file_path)


def refine(constraint_id_to_system, constraint_to_operand, escs, special_characters_flag, camel_case_flag):
    # ESC refinement: process the extracted ESC using the constraints_to_ddc

    refined_escs = {}
    for constraint, constraint_to_ddcs in constraint_to_operand.items():
        start_time = time.time()
        generate_esc_to_constraint(refined_escs, constraint, constraint_to_ddcs,
                                   [el for el in escs if el[0] == constraint_id_to_system[constraint]],
                                   special_characters_flag, camel_case_flag)
        print("--- Generated constraint: ", constraint, ", ESCs: ", len(refined_escs[constraint]),
              " in %s seconds ---" % (time.time() - start_time))

    return refined_escs


def generate_esc_to_constraint(refined_escs, constraint, constraint_to_ddcs, escs, special_characters_flag,
                               camel_case_flag):
    temp_esc = []
    ddcs_by_operand = list(constraint_to_ddcs.values())
    ddcs_operands = list(constraint_to_ddcs.keys())

    # for esc in escs:
    #     if all(any(term in esc[6].lower() for term in lst) for lst in (ddcs_by_operand[0], ddcs_by_operand[1])):
    #         temp_esc.append(esc)
    # refined_escs[constraint] = temp_esc

    for esc in escs:
        # check in case one of the operands is in the unimplemented list to only refine for the other
        if ddcs_operands[0] in UNIMPLEMENTED_OPERANDS_3:
            if any(term in esc[6].lower() for term in constraint_to_ddcs[ddcs_operands[1]]):
                temp_esc.append(esc)
        elif ddcs_operands[1] in UNIMPLEMENTED_OPERANDS_3:
            if any(term in esc[6].lower() for term in constraint_to_ddcs[ddcs_operands[0]]):
                temp_esc.append(esc)
        else:
            # At least one token1/token2 in ESC
            # (token1 in esc) OR (token2 in esc)
            # if any(any(term in esc[6].lower() for term in lst) for lst in (ddcs_by_operand[0], ddcs_by_operand[1])):
            # Both token1/token2 in ESC
            # (token1 in esc) AND (token2 in esc)
            if all(any(term in esc[6].lower() for term in lst) for lst in (ddcs_by_operand[0], ddcs_by_operand[1])):
                temp_esc.append(esc)
    refined_escs[constraint] = temp_esc

    # # filter after the system
    # for esc in escs:
    #     # for each operand we have list of possible DDCs
    #     if ddcs_by_operand[1]:
    #         # for ddc1 in [el for el in ddcs_by_operand[0] if el[0] == esc[0]]:
    #         #     for ddc2 in [el for el in ddcs_by_operand[1] if el[0] == esc[0]]:
    #         # todo: switch between using the ddc and the tokens
    #         # for ddc1 in ddcs_by_operand[0]:
    #         #     for ddc2 in ddcs_by_operand[1]:
    #         #         if String_Comparator.check_similarity_esc_ddc(esc, ddc1, special_characters_flag, camel_case_flag) \
    #         #                 and String_Comparator.check_similarity_esc_ddc(esc, ddc2, special_characters_flag, camel_case_flag):
    #         #             temp_esc.append(esc)
    #         # todo: equivalence between the fors and the if all/any
    #         if all(any(String_Comparator.check_similarity_esc_ddc(esc, term, special_characters_flag, camel_case_flag) for term in lst) for lst in (ddcs_by_operand[0], ddcs_by_operand[1])):
    #             temp_esc.append(esc)
    #     else:
    #         # for ddc in [el for el in ddcs_by_operand[0] if el[0] == esc[0]]:
    #         # todo: switch between using the ddc and the tokens
    #         for ddc in ddcs_by_operand[0]:
    #             if String_Comparator.check_similarity_esc_ddc(esc, ddc, special_characters_flag, camel_case_flag):
    #                 temp_esc.append(esc)
    # refined_escs[constraint] = temp_esc


def get_statistics(escs, constraints, refine_method):
    header = ['constraint', '# of results', 'matched ? 1/0']

    statistics_path_refined = statistics_path.split(".")[0] + '_refine' + refine_method.__str__() \
                              + "_UNIMPLEMENTED_OPS_All" + "." + statistics_path.split(".")[1]

    # open the file in the write mode
    with open(statistics_path_refined, 'w') as f:
        writer = csv.writer(f)
        # write the header
        writer.writerow(header)

        for constraint in constraints:
            matched = 0
            for esc in escs[constraint[0]]:
                if esc[2] in constraint[1] and esc[3].split(":")[0] in constraint[1]:
                    matched = 1
            # write the data
            writer.writerow([constraint[0], len(escs[constraint[0]]), matched])
