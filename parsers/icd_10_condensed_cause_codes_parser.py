from definitions import RESOURCES_DIR
import csv


def get_icd10_condensed_cause_code_dict():
    """
    Creates a dictionary of code-cause key-value pairs using the condensed, integer only format contained in the ICD10
    cause code table.

    See Table 8 for further details - https://www.who.int/healthinfo/statistics/documentation

    :return: {code: cause} dict
    """
    cause_codes_path = RESOURCES_DIR + r"/ICD10_list_101_103_cause_codes.csv"
    cc_dict = {}
    with open(cause_codes_path, 'r', encoding='utf-8') as f:
        csv_reader = csv.reader(f, delimiter=',')
        next(csv_reader, None)
        for row in csv_reader:
            cc_dict[row[0]] = row[2]
    return cc_dict


def get_icd10_portugal_condensed_cause_code_dict():
    """
    Creates a dictionary of code-cause key-value pairs using the condensed, integer only format contained in the
    "ICD 10 special list for Portugal - data for 2004-2005" cause code table.

    See Table 10 for further details - https://www.who.int/healthinfo/statistics/documentation

    :return: {code: cause} dict
    """
    cause_codes_path = RESOURCES_DIR + r"/ICD10_list_UE1_cause_codes.csv"

    cc_dict = {}
    with open(cause_codes_path, 'r', encoding='utf-8') as f:
        csv_reader = csv.reader(f, delimiter=',')
        next(csv_reader, None)
        for row in csv_reader:
            cc_dict[row[0]] = row[2]
    return cc_dict
