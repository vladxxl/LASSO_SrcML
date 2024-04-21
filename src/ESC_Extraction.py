import csv
import os
import re
import xml.etree.ElementTree as ET
import subprocess


save_to_file_path = 'intermediary/ESC_Extraction.csv'
statistics_path = 'intermediary/ESC_Extraction_Statistics.csv'


def clean_xml_namespaces(root):
    for elem in root.iter():
        elem.tag = re.sub(r"\{(.*?)\}", "", elem.tag)


def extract(folder, save_option):
    # check for saved data for ease of execution
    if save_option and os.path.exists(save_to_file_path) and os.path.getsize(save_to_file_path) > 0:
        with open(save_to_file_path) as fp:
            reader = csv.reader(fp, delimiter=",", quotechar='"')
            next(reader, None)  # skip the headers
            cips = [row for row in reader]
        return cips

    # read the input systems
    sub_folders = [name for name in os.listdir(folder) if os.path.isdir(os.path.join(folder, name))]

    # read the CIPs
    cips = []
    with open('src/CIP.csv') as fp:
        reader = csv.reader(fp, delimiter=";")
        cips = [row for row in reader]

    # ESC extraction
    escs = []
    for system in sub_folders:
        # construct the ESCs
        for root, dirs, files in os.walk(folder + '/' + system):
            for file in files:
                if file.endswith(".java"):
                    # check to exclude test cases
                    if 'test' in root:
                        break

                    for cip in cips:
                        # apply srcML with the position and XPath option to extract the ESC with the necessary metadata
                        srcML = subprocess.Popen(["srcml", "--position", "--xpath", cip[1], os.path.join(root, file)],
                                                 stdout=subprocess.PIPE)
                        output = srcML.communicate()[0]

                        # use ElementTree to parse result of the with XPath queries
                        tree = ET.fromstring(output)
                        clean_xml_namespaces(tree)

                        for elem in tree.iterfind('.//unit/*'):
                            # print([xml_file, ddp[0], ''.join(elem.itertext())])
                            # [ path, java_file, start_pos, end_pos, DDP, code]
                            if len(elem.attrib) >= 2:
                                escs.append([system, root, file, elem.attrib['{http://www.srcML.org/srcML/position}start'],
                                     elem.attrib['{http://www.srcML.org/srcML/position}end'], cip[0],
                                     ''.join(elem.itertext())])

    if save_option and len(escs) > 0:
        header = ['system', 'path', 'java_file', 'start_pos', 'end_pos', 'CIP', 'code']
        # open the file in the write mode
        with open(save_to_file_path, 'w') as f:
            writer = csv.writer(f)
            # write the header
            writer.writerow(header)
            for esc in escs:
                # write the data
                writer.writerow(esc)

    return escs


# ESC: system, path, java_file, start_pos, end_pos, CIP, code
def print_esc(escs):
    # unique values for the system
    values = set([el[0] for el in escs])
    print('-------------------')
    for elem in values:
        # print(elem)
        print(len([el for el in escs if el[0] == elem]), ':', elem)
    print('-------------------')
    print()
    # group DDCs by the system
    # newlist = [[y for y in ddcs if y[0] == x] for x in values]


def get_statistics(escs, constraints):
    systems = list(set([el[0] for el in escs]))
    patterns = list(set([el[5] for el in escs]))
    # escs_by_system = [[y for y in ddcs if y[0] == x] for x in systems]
    escs_by_system_by_pattern = [[[el for el in escs if el[5] == pattern and el[0] == system] for pattern in patterns] for system in systems]

    constraints_esc_by_system_by_pattern = [[[el for el in constraints if re.sub("-", "_", el[3]).upper() == pattern and el[1] == system] for pattern in patterns] for system in systems]

    # header = ['system', 'CIP', '# of results', '# of constraints', '# of matches', 'flag']
    header = ['system', 'CIP', '# of results', '# of input constraints', '# of matches']

    # open the file in the write mode
    with open(statistics_path, 'w') as f:
        writer = csv.writer(f)
        # write the header
        writer.writerow(header)

        for i in range(len(systems)):
            for j in range(len(patterns)):
                no_of_matches = 0
                for constraint in constraints_esc_by_system_by_pattern[i][j]:
                    matched = False
                    for extracted in escs_by_system_by_pattern[i][j]:
                        java_file_start_pos = extracted[2] + ':' + extracted[3].split(':')[0]
                        if java_file_start_pos in constraint[2] or java_file_start_pos in constraint[3]:
                            no_of_matches += 1
                            matched = True
                    # debug
                    if not matched:
                        print(constraint)
                flag = ''
                if no_of_matches < len(constraints_esc_by_system_by_pattern[i][j]):
                    flag = '!'

                # write the data
                writer.writerow([systems[i], patterns[j], len(escs_by_system_by_pattern[i][j]), len(constraints_esc_by_system_by_pattern[i][j]), no_of_matches, flag])