import unittest
from unittest.mock import patch
import pandas as pd
from definitions import TEST_RESOURCES
from pipeline.ingest import icd10_mortality_rates_processor


class ICD10IngestTestCase(unittest.TestCase):

    @patch('pipeline.ingest.icd10_mortality_rates_processor.download_file')
    @patch('pipeline.ingest.icd10_mortality_rates_processor.unzip_file')
    def test_icd10_mortality_rates_ingest_success(self, mock_unzip_file, mock_download_file):
        mock_unzip_file.return_value = TEST_RESOURCES + '/mock_icd10_input_csv.csv'
        mock_download_file.return_value = 'test'

        columns = ['country', 'year', 'cause', 'sex', 'deaths']
        input_data = [['Algeria', 2001, 'Cholera', 'f', 12],
                     ['Algeria', 2001, 'Cholera', 'm', 10],
                     ['Algeria', 2002, 'Tetanus', 'f', 2],
                     ['Algeria', 2002, 'Tetanus', 'm', 4],
                     ['France', 2001, 'Schistosomiasis', 'f', 14],
                     ['France', 2001, 'Schistosomiasis', 'm', 14],
                     ['Italy', 2002, 'Plague', 'm', 4],
                     ['Lithuania', 2002, 'Plague', 'f', 5]]

        expected_output_df = pd.DataFrame(input_data, columns=columns)

        pd.testing.assert_frame_equal(icd10_mortality_rates_processor.run('test_url'),
                                      expected_output_df,
                                      check_dtype=False)


if __name__ == '__main__':
    unittest.main()
