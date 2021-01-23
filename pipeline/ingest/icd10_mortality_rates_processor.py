import requests
import zipfile
import logging
from tqdm import tqdm
import pandas as pd
from pipeline.parsers import icd_10_code_parsers


module_logger = logging.getLogger(__name__)


def download_file(url):
    module_logger.info(f"Downloading file from {url}...")
    local_filename = url.split('/')[-1]
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            progress_bar = tqdm(total=int(r.headers['Content-Length']))
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
                progress_bar.update(len(chunk))
    progress_bar.clear()
    module_logger.info(f"Download complete, file saved as: {local_filename}")
    return local_filename


def unzip_file(zip_file_path):
    module_logger.info(f"Extracting {zip_file_path}...")
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall("./")
    module_logger.info(f"Extraction complete, file saved as {zip_ref.filename.split('.')[0]}")
    return zip_ref.filename.split(".")[0]


def run(mortality_data_url):
    """
    Downloads ICD10 mortality rates data from WHO servers, cleans and transforms data, and returns processed DataFrame.

    :return: Processed ICD10 mortality rates DataFrame
    """

    module_logger.info(f"Starting ICD10 processor for {mortality_data_url}...")
    # Download pt1 of data
    mortality_rates_zip_name = download_file(mortality_data_url)

    # Extract data
    mortality_rates_name = unzip_file(mortality_rates_zip_name)

    # Read into dataframe
    module_logger.info(f"Reading {mortality_rates_name} into DataFrame...")
    mortality_df = pd.read_csv(mortality_rates_name, dtype={'Country': int,
                                                            'Year': int,
                                                            'Sex': int,
                                                            'Deaths1': int})

    module_logger.info("Processing ICD 10 DataFrame...")

    # Remove unneeded columns
    mortality_df = mortality_df[['Country', 'Year', 'List', 'Cause', 'Sex', 'Deaths1']]

    # Rename columns to lowercase
    mortality_df.rename(columns={'Country': 'country',
                                 'Year': 'year',
                                 'List': 'list',
                                 'Cause': 'cause',
                                 'Sex': 'sex',
                                 'Deaths1': 'deaths'}, inplace=True)

    # Map sex codes to characters
    mortality_df['sex'] = mortality_df['sex'].map({1: 'm',
                                                   2: 'f',
                                                   9: 'u'})

    # Map county codes to country names
    mortality_df['country'] = mortality_df['country'].map(icd_10_code_parsers.get_country_codes_dict())

    # Map ICD10 condensed cause codes to cause names
    icd_10_condensed_dict = icd_10_code_parsers.get_condensed_cause_code_dict()
    mortality_df.loc[mortality_df['list'] == 101, 'cause'] = \
        mortality_df.loc[mortality_df['list'] == 101, 'cause'].map(icd_10_condensed_dict)

    # Map ICD10 (revision 3) character cause codes to cause names
    icd_10_3_char_dict = icd_10_code_parsers.get_3_char_cause_code_dict()
    mortality_df.loc[mortality_df['list'] == '103', 'list'] = 103
    mortality_df.loc[mortality_df['list'] == 103, 'cause'] = \
        mortality_df.loc[mortality_df['list'] == 103, 'cause'].map(icd_10_3_char_dict)

    # Map ICD10 (revision 4) character cause codes to cause names
    mortality_df.loc[mortality_df['list'] == '104', 'list'] = 104
    mortality_df.loc[mortality_df['list'] == 104, 'cause'] = \
        mortality_df.loc[mortality_df['list'] == 104, 'cause'].map(lambda x: x[:3]).map(icd_10_3_char_dict)

    # Map ICD10 (revision 10M)) character cause codes to cause names
    mortality_df.loc[mortality_df['list'] == '10M', 'cause'] = \
        mortality_df.loc[mortality_df['list'] == '10M', 'cause'].map(lambda x: x[:3]).map(icd_10_3_char_dict)

    # Map ICD10 (revision Portugal special list) character cause codes to cause names
    icd_10_portugal_codes_dict = icd_10_code_parsers.get_portugal_condensed_cause_code_dict()
    mortality_df.loc[mortality_df['list'] == 'UE1', 'cause'] = \
        mortality_df.loc[mortality_df['list'] == 'UE1', 'cause'].map(icd_10_portugal_codes_dict)

    # No longer need List column so will drop
    mortality_df.drop(columns='list', inplace=True)

    # Aggregating duplicate rows by combining deaths
    module_logger.info("Aggregating data...")
    mortality_df = mortality_df.groupby(by=['country', 'year', 'cause', 'sex'], as_index=False).sum()

    return mortality_df
