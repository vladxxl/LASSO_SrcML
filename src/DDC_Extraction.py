import csv
import os
import re
import xml.etree.ElementTree as ET
import subprocess


save_to_file_path = 'intermediary/DDC_Extraction.csv'
statistics_path = 'intermediary/DDC_Extraction_Statistics.csv'


def clean_xml_namespaces(root):
    for elem in root.iter():
        elem.tag = re.sub(r"\{(.*?)\}", "", elem.tag)


def extract(folder, save_option):
    # check for saved data for ease of execution
    if os.path.exists(save_to_file_path) and os.path.getsize(save_to_file_path) > 0:
        with open(save_to_file_path) as fp:
            reader = csv.reader(fp, delimiter=",", quotechar='"')
            next(reader, None)  # skip the headers
            ddcs = [row for row in reader]
        return ddcs

    # read the input systems
    sub_folders = [name for name in os.listdir(folder) if os.path.isdir(os.path.join(folder, name))]

    # read the DDPs
    ddps = []
    with open('src/DDP.csv') as fp:
        reader = csv.reader(fp, delimiter=";")
        ddps = [row for row in reader]

    # DDC extraction
    ddcs = []
    for system in sub_folders:
        # construct the DDCs
        for root, dirs, files in os.walk(folder + '/' + system):
            for file in files:
                if file.endswith(".java"):
                    # check to exclude test cases
                    if 'test' in root:
                        break

                    for ddp in ddps:
                        # apply srcML with the position and XPath option to extract the DDC with the necessary metadata
                        srcML = subprocess.Popen(["srcml", "--position", "--xpath", ddp[1], os.path.join(root, file)],
                                                 stdout=subprocess.PIPE)
                        output = srcML.communicate()[0]

                        # use ElementTree to parse result of the with XPath queries
                        tree = ET.fromstring(output)
                        clean_xml_namespaces(tree)

                        for elem in tree.iterfind('.//unit/*'):
                            # print([xml_file, ddp[0], ''.join(elem.itertext())])
                            # [ path, java_file, start_pos, end_pos, DDP, code]
                            if len(elem.attrib) >= 2:
                                ddcs.append([system, root, file, elem.attrib['{http://www.srcML.org/srcML/position}start'],
                                     elem.attrib['{http://www.srcML.org/srcML/position}end'], ddp[0],
                                     ''.join(elem.itertext())])

    if save_option and len(ddcs) > 0:
        header = ['system', 'path', 'java_file', 'start_pos', 'end_pos', 'DDP', 'code']
        # open the file in the write mode
        with open(save_to_file_path, 'w') as f:
            writer = csv.writer(f)
            # write the header
            writer.writerow(header)
            for ddc in ddcs:
                # write the data
                writer.writerow(ddc)

    return ddcs


# DDC: system, path, java_file, start_pos, end_pos, DDP, code
def print_ddc(ddcs):
    # unique values for the system
    values = set([el[0] for el in ddcs])
    print('-------------------')
    for elem in values:
        # print(elem)
        print(len([el for el in ddcs if el[0] == elem]), ':', elem)
    print('-------------------')
    print()
    # group DDCs by the system
    # newlist = [[y for y in ddcs if y[0] == x] for x in values]


def get_statistics(ddcs, constraints):
    systems = list(set([el[0] for el in ddcs]))
    patterns = list(set([el[5] for el in ddcs]))
    # ddcs_by_system = [[y for y in ddcs if y[0] == x] for x in systems]
    ddcs_by_system_by_pattern = [[[el for el in ddcs if el[5] == pattern and el[0] == system] for pattern in patterns] for system in systems]

    constraints_ddc_by_system_by_pattern = [[[el for el in constraints if (el[4] == pattern or el[5] == pattern) and (el[1] == system)] for pattern in patterns] for system in systems]

    # header = ['system', 'DDP', '# of results', '# of constraints', '# of matches', 'flag']
    header = ['system', 'DDP', '# of results', '# of input constraints', '# of matches']

    # open the file in the write mode
    with open(statistics_path, 'w') as f:
        writer = csv.writer(f)
        # write the header
        writer.writerow(header)

        for i in range(len(systems)):
            for j in range(len(patterns)):
                no_of_matches = 0
                for constraint in constraints_ddc_by_system_by_pattern[i][j]:
                    for extracted in ddcs_by_system_by_pattern[i][j]:
                        java_file_start_pos = extracted[2] + ':' + extracted[3].split(':')[0]
                        if java_file_start_pos in constraint[2] or java_file_start_pos in constraint[3]:
                            no_of_matches += 1
                flag = ''
                if no_of_matches < len(constraints_ddc_by_system_by_pattern[i][j]):
                    flag = '!'

                # write the data
                writer.writerow([ddcs_by_system_by_pattern[i][j][0][0], ddcs_by_system_by_pattern[i][j][0][5], len(ddcs_by_system_by_pattern[i][j]), len(constraints_ddc_by_system_by_pattern[i][j]), no_of_matches, flag])
