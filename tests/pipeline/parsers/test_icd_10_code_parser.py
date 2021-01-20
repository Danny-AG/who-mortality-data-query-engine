import unittest
from unittest.mock import patch
from definitions import TEST_RESOURCES
from pipeline.parsers.icd_10_code_parsers import extract_char_numeral_pair
from pipeline.parsers.icd_10_code_parsers import code_range_str_to_list
from pipeline.parsers.icd_10_code_parsers import detailed_code_str_to_list
from pipeline.parsers.icd_10_code_parsers import get_3_char_cause_code_dict
from pipeline.parsers.icd_10_code_parsers import get_condensed_cause_code_dict
from pipeline.parsers.icd_10_code_parsers import get_portugal_condensed_cause_code_dict
from pipeline.parsers.icd_10_code_parsers import get_country_codes_dict


class ExtractCharNumeralPairTestCase(unittest.TestCase):
    def test_valid_input_str(self):
        input_code_str = 'A01'
        expected_output = ('A', '01')
        self.assertEqual(extract_char_numeral_pair(input_code_str), expected_output)

    def test_invalid_input_str_bad_pattern(self):
        input_code_str = 'AAA'
        with self.assertRaises(ValueError):
            extract_char_numeral_pair(input_code_str)

        input_code_str = 'A010'
        with self.assertRaises(ValueError):
            extract_char_numeral_pair(input_code_str)

        input_code_str = 'a01'
        with self.assertRaises(ValueError):
            extract_char_numeral_pair(input_code_str)

        input_code_str = '&18'
        with self.assertRaises(ValueError):
            extract_char_numeral_pair(input_code_str)

    def test_invalid_input_str_wrong_type(self):
        input_code_str = 1
        with self.assertRaises(TypeError):
            extract_char_numeral_pair(input_code_str)

        input_code_str = None
        with self.assertRaises(TypeError):
            extract_char_numeral_pair(input_code_str)


class CodeRangeStrToListTestCase(unittest.TestCase):
    def test_valid_code_range_str(self):
        input_str = 'A98-B03'
        expected_output = ['A98', 'A99', 'B00', 'B01', 'B02', 'B03']
        self.assertEqual(code_range_str_to_list(input_str), expected_output)

        input_str = 'A98-A99'
        expected_output = ['A98', 'A99']
        self.assertEqual(code_range_str_to_list(input_str), expected_output)

    def test_valid_code_range_single_code(self):
        input_str = "A99"
        expected_output = ['A99']
        self.assertEqual(code_range_str_to_list(input_str), expected_output)

    def test_invalid_code_range_bad_pattern(self):
        input_str = "abcd"
        with self.assertRaises(ValueError):
            code_range_str_to_list(input_str)

        input_str = "A98-B0100"
        with self.assertRaises(ValueError):
            code_range_str_to_list(input_str)

    def test_invalid_code_range_backwards_range(self):
        input_str = 'B02-A98'
        with self.assertRaises(ValueError):
            code_range_str_to_list(input_str)

    def test_invalid_code_range_wrong_type(self):
        input_str = 1
        with self.assertRaises(TypeError):
            code_range_str_to_list(input_str)

        input_str = None
        with self.assertRaises(TypeError):
            code_range_str_to_list(input_str)


class DetailedCodeStrToListTestCase(unittest.TestCase):
    def test_valid_list_numbers_str(self):
        input_str = 'A98-B03, B06-B07'
        expected_output = ['A98', 'A99', 'B00', 'B01', 'B02', 'B03', 'B06', 'B07']
        self.assertEqual(detailed_code_str_to_list(input_str), expected_output)

        input_str = 'A98-B03, B06'
        expected_output = ['A98', 'A99', 'B00', 'B01', 'B02', 'B03', 'B06']
        self.assertEqual(detailed_code_str_to_list(input_str), expected_output)

        input_str = 'A98-B03'
        expected_output = ['A98', 'A99', 'B00', 'B01', 'B02', 'B03']
        self.assertEqual(detailed_code_str_to_list(input_str), expected_output)

        input_str = 'A98'
        expected_output = ['A98']
        self.assertEqual(detailed_code_str_to_list(input_str), expected_output)

    def test_invalid_list_numbers_str_wrong_format(self):
        input_str = 'aaa'
        with self.assertRaises(ValueError):
            detailed_code_str_to_list(input_str)

        input_str = 'B01-A99'
        with self.assertRaises(ValueError):
            detailed_code_str_to_list(input_str)

        input_str = 'A0000'
        with self.assertRaises(ValueError):
            detailed_code_str_to_list(input_str)

        input_str = 'A97-a'
        with self.assertRaises(ValueError):
            detailed_code_str_to_list(input_str)

        input_str = 'AAA-BBB'
        with self.assertRaises(ValueError):
            detailed_code_str_to_list(input_str)

    def test_invalid_list_numbers_str_wrong_type(self):
        input_str = 1
        with self.assertRaises(TypeError):
            detailed_code_str_to_list(input_str)

        input_str = None
        with self.assertRaises(TypeError):
            detailed_code_str_to_list(input_str)


class Get3CharCauseCodeDictTestCase(unittest.TestCase):

    @patch('pipeline.parsers.icd_10_code_parsers.ICD_10_CAUSE_CODES_PATH', TEST_RESOURCES + '/mock_cause_codes.csv')
    def test_successful_dict_return(self):

        expected_output = {'A95': 'Cholera',
                           'A96': 'Diarrhoea',
                           'A97': 'Other infectious diseases',
                           'A98': 'Other infectious diseases',
                           'A99': 'Other infectious diseases',
                           'B00': 'Other infectious diseases',
                           'B01': 'Certain infectious and parasitic diseases',
                           'B02': 'Remainder of diseases',
                           'B03': 'Remainder of diseases',
                           'B04': 'Certain infectious and parasitic diseases',
                           'B05': 'Remainder of diseases',
                           'B06': 'Certain infectious and parasitic diseases',
                           'B07': 'Remainder of diseases',
                           'B08': 'Remainder of diseases',
                           'B09': 'Certain infectious and parasitic diseases',
                           'B10': 'Certain infectious and parasitic diseases'}

        self.assertEqual(get_3_char_cause_code_dict(), expected_output)


class GetCondensedCauseCodeDictTestCase(unittest.TestCase):

    @patch('pipeline.parsers.icd_10_code_parsers.ICD_10_CAUSE_CODES_PATH', TEST_RESOURCES + '/mock_cause_codes.csv')
    def test_successful_dict_return(self):

        expected_output = {'1000': 'All causes',
                           '1001': 'Certain infectious and parasitic diseases',
                           '1002': 'Cholera',
                           '1003': 'Diarrhoea',
                           '1004': 'Other infectious diseases',
                           '1005': 'Remainder of diseases'}

        self.assertEqual(get_condensed_cause_code_dict(), expected_output)


class GetPortugalCondensedCauseCodeDictTestCase(unittest.TestCase):

    @patch('pipeline.parsers.icd_10_code_parsers.ICD_10_PORTUGAL_CAUSE_CODES_PATH',
           TEST_RESOURCES + '/mock_portugal_cause_codes.csv')
    def test_successful_dict_return(self):

        expected_output = {'CH00': 'All causes',
                           'CH01': 'Certain infectious and parasitic diseases',
                           'UE02': 'Cholera',
                           'UE03': 'Diarrhoea'}

        self.assertEqual(get_portugal_condensed_cause_code_dict(), expected_output)


class GetCountryCodesTestCase(unittest.TestCase):

    @patch('pipeline.parsers.icd_10_code_parsers.COUNTRY_CODES_PATH',
           TEST_RESOURCES + '/mock_country_codes.csv')
    def test_successful_dict_return(self):

        expected_output = {1010: 'Algeria',
                           1020: 'Angola',
                           1025: 'Benin',
                           1030: 'Botswana',
                           1035: 'Burkina Faso'}

        self.assertEqual(get_country_codes_dict(), expected_output)


if __name__ == '__main__':
    unittest.main()
