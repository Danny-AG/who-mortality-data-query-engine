import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
RESOURCES_DIR = ROOT_DIR + "/resources"

ICD_10_CAUSE_CODES_PATH = RESOURCES_DIR + r"/ICD10_list_101_103_cause_codes.csv"
ICD_10_PORTUGAL_CAUSE_CODES_PATH = RESOURCES_DIR + r"/ICD10_list_UE1_cause_codes.csv"
COUNTRY_CODES_PATH = RESOURCES_DIR + "/country_codes/country_codes"

TEST_RESOURCES = RESOURCES_DIR + '/test_files'
