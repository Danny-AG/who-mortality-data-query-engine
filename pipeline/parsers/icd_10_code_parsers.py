import csv
import re
import pandas as pd
import logging
from definitions import RESOURCES_DIR


module_logger = logging.getLogger(__name__)

# Regex's used for parsing codes
cause_code_split_regex = re.compile(r"([A-Z]{1})([0-9]{2})")
ranged_cause_code_validity_regex = re.compile(r"[A-Z]{1}[0-9]{2}-[A-Z]{1}[0-9]{2}")


def extract_char_numeral_pair(code_str):
    """
    Extract the character and number from strings of the format [char][num][num]

    Example:
    input = 'A01'
    output = ('A', '01')

    :param code_str: str
    :return: Tuple(str, str)
    """
    match = cause_code_split_regex.match(code_str)
    if match:
        return match.groups()
    else:
        raise ValueError(f"Unable to extract char and numeral from {code_str}")


def code_range_str_to_list(cause_code_range_str):
    """
    Converts a code string range to a list of individual codes.

    Example:
    input = 'A98-B03'
    output = ['A98', 'A99', 'B01', 'B02', 'B03']

    :param cause_code_range_str: str
    :return: List[str]
    """
    if ranged_cause_code_validity_regex.match(cause_code_range_str) is None:
        return [cause_code_range_str]

    start_code, end_code = cause_code_range_str.split('-')

    try:
        start_char, start_num = extract_char_numeral_pair(start_code)
        end_char, end_num = extract_char_numeral_pair(end_code)
    except ValueError as e:
        print(f"Failed to generate list between codes {start_code} and {end_code}.\n{e}")
        raise

    output_list = []

    current_char = start_char
    current_num = int(start_num)
    output_list.append(current_char + str(current_num).zfill(2))
    while True:
        current_num += 1
        if current_num >= 100:
            current_num = 0
            current_char = chr(ord(current_char) + 1)

        output_list.append(current_char + str(current_num).zfill(2))
        if current_char == end_char and str(current_num).zfill(2) == end_num:
            break

    return output_list


def detailed_code_str_to_list(detailed_list_numbers_str):
    """
    Converts a code string (including jumps in ranges) to a list of individual codes.

    Example:
    input = 'A98-B03, B06-B07'
    output = ['A98', 'A99', 'B01', 'B02', 'B03', 'B06', 'B07']

    :param detailed_list_numbers_str: str
    :return:
    """
    codes = []
    for code_range_str in detailed_list_numbers_str.replace(' ', '').split(','):
        codes.extend(code_range_str_to_list(code_range_str))

    return codes


def get_3_char_cause_code_dict():
    """
    Creates a dictionary of code-cause key-value pairs using the 3 character code formats contained in the ICD10 cause
    code table.

    See Table 8 for further details - https://www.who.int/healthinfo/statistics/documentation

    :return: {code: cause} dict
    """
    module_logger.debug("Getting ICD10 3 character code format cause codes.")

    cause_codes_path = RESOURCES_DIR + r"/ICD10_list_101_103_cause_codes.csv"
    cause_codes_df = pd.read_csv(cause_codes_path, dtype={'code': int,
                                                          'Detailed List Numbers': str,
                                                          'Cause': str}).rename(
        columns={'Detailed List Numbers': 'detailed_codes',
                 'Cause': 'cause'})

    cause_codes_df['detailed_codes'] = cause_codes_df[cause_codes_df['detailed_codes'].notna()]['detailed_codes'].apply(
        detailed_code_str_to_list)

    detailed_code_cause_dict = {}
    for row in cause_codes_df[cause_codes_df['detailed_codes'].notna()].itertuples():
        for code in row.detailed_codes:
            detailed_code_cause_dict[code] = row.cause

    return detailed_code_cause_dict


def get_condensed_cause_code_dict():
    """
    Creates a dictionary of code-cause key-value pairs using the condensed, integer only format contained in the ICD10
    cause code table.

    See Table 8 for further details - https://www.who.int/healthinfo/statistics/documentation

    :return: {code: cause} dict
    """
    module_logger.debug("Getting ICD10 condensed format cause codes.")

    cause_codes_path = RESOURCES_DIR + r"/ICD10_list_101_103_cause_codes.csv"
    cc_dict = {}
    with open(cause_codes_path, 'r', encoding='utf-8') as f:
        csv_reader = csv.reader(f, delimiter=',')
        next(csv_reader, None)
        for row in csv_reader:
            cc_dict[row[0]] = row[2]
    return cc_dict


def get_portugal_condensed_cause_code_dict():
    """
    Creates a dictionary of code-cause key-value pairs using the condensed, integer only format contained in the
    "ICD 10 special list for Portugal - data for 2004-2005" cause code table.

    See Table 10 for further details - https://www.who.int/healthinfo/statistics/documentation

    :return: {code: cause} dict
    """
    module_logger.debug("Getting ICD10 special list for Portugal format cause codes.")

    cause_codes_path = RESOURCES_DIR + r"/ICD10_list_UE1_cause_codes.csv"

    cc_dict = {}
    with open(cause_codes_path, 'r', encoding='utf-8') as f:
        csv_reader = csv.reader(f, delimiter=',')
        next(csv_reader, None)
        for row in csv_reader:
            cc_dict[row[0]] = row[2]
    return cc_dict


def get_country_codes_dict():
    """
    Creates a dictionary of code-country key-value pairs using the country codes csv.

    See Table 11 for further details - https://www.who.int/healthinfo/statistics/documentation

    :return: {code: country} dict
    """
    module_logger.debug("Getting ICD10 country codes.")

    country_codes_path = RESOURCES_DIR + "/country_codes/country_codes"
    country_codes_dict = {}

    with open(country_codes_path, 'r', encoding='utf-8') as f:
        csvreader = csv.reader(f, delimiter=',')
        next(csvreader, None)
        for row in csvreader:
            country_codes_dict[int(row[0])] = row[1]

    return country_codes_dict
