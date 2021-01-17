import unittest
from pipeline.parsers.icd_10_code_parsers import extract_char_numeral_pair
from pipeline.parsers.icd_10_code_parsers import code_range_str_to_list
from pipeline.parsers.icd_10_code_parsers import detailed_code_str_to_list
from pipeline.parsers.icd_10_code_parsers import get_3_char_cause_code_dict


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


if __name__ == '__main__':
    unittest.main()
