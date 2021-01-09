import requests
import zipfile
import logging
from tqdm import tqdm
import pandas as pd
from parsers import icd_10_parsers


def download_file(url):
    logging.info(f"Downloading from {url}...")
    local_filename = url.split('/')[-1]
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            progress_bar = tqdm(total=int(r.headers['Content-Length']))
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
                progress_bar.update(len(chunk))
    progress_bar.clear()
    logging.info(f"Download complete, file saved as: {local_filename}")
    return local_filename


def unzip_file(zip_file_path):
    logging.info(f"Extracting {zip_file_path}...")
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall("./")
    logging.info(f"Extraction complete, file saved as {zip_ref.filename.split('.')[0]}")
    return zip_ref.filename.split(".")[0]


logging.basicConfig(level=logging.DEBUG, format='%(name)s - %(levelname)s - %(message)s')

# Download pt1 of data
who_mortality_rates_url = "https://www.who.int/healthinfo/statistics/Morticd10_part1.zip"
who_mortality_rates_zip_name = download_file(who_mortality_rates_url)

# Extract data
who_mortality_rates_name = unzip_file(who_mortality_rates_zip_name)

# Read into dataframe
logging.info(f"Reading {who_mortality_rates_name} into DataFrame...")
mortality_pt1_df = pd.read_csv(who_mortality_rates_name, dtype={'Country': int,
                                                                'Year': int,
                                                                'Sex': int,
                                                                'Deaths1': int})

# Remove unneeded columns
mortality_pt1_df = mortality_pt1_df[['Country', 'Year', 'List', 'Cause', 'Sex', 'Deaths1']]

# Map sex codes to characters
mortality_pt1_df['Sex'] = mortality_pt1_df['Sex'].map({1: 'm',
                                                       2: 'f',
                                                       9: 'u'})

# Map county codes to country names
mortality_pt1_df['Country'] = mortality_pt1_df['Country'].map(icd_10_parsers.get_country_codes_dict())

# Map ICD10 condensed cause codes to cause names
icd_10_condensed_dict = icd_10_parsers.get_condensed_cause_code_dict()
mortality_pt1_df.loc[mortality_pt1_df['List'] == 101, 'Cause'] = \
    mortality_pt1_df.loc[mortality_pt1_df['List'] == 101, 'Cause'].map(icd_10_condensed_dict)

# Map ICD10 (revision 3) character cause codes to cause names
icd_10_3_char_dict = icd_10_parsers.get_3_char_cause_code_dict()
mortality_pt1_df.loc[mortality_pt1_df['List'] == '103', 'List'] = 103
mortality_pt1_df.loc[mortality_pt1_df['List'] == 103, 'Cause'] = \
    mortality_pt1_df.loc[mortality_pt1_df['List'] == 103, 'Cause'].map(icd_10_3_char_dict)

# Map ICD10 (revision 4) character cause codes to cause names
mortality_pt1_df.loc[mortality_pt1_df['List'] == '104', 'List'] = 104
mortality_pt1_df.loc[mortality_pt1_df['List'] == 104, 'Cause'] = \
    mortality_pt1_df.loc[mortality_pt1_df['List'] == 104, 'Cause'].map(lambda x: x[:3]).map(icd_10_3_char_dict)

# Map ICD10 (revision 10M)) character cause codes to cause names
mortality_pt1_df.loc[mortality_pt1_df['List'] == '10M', 'Cause'] = \
    mortality_pt1_df.loc[mortality_pt1_df['List'] == '10M', 'Cause'].map(lambda x: x[:3]).map(icd_10_3_char_dict)

# Map ICD10 (revision Portugal special list) character cause codes to cause names
icd_10_portugal_codes_dict = icd_10_parsers.get_portugal_condensed_cause_code_dict()
mortality_pt1_df.loc[mortality_pt1_df['List'] == 'UE1', 'Cause'] = \
    mortality_pt1_df.loc[mortality_pt1_df['List'] == 'UE1', 'Cause'].map(icd_10_portugal_codes_dict)

# Write dataframe to database

# Clean out saved data and dataframes to save space

# If dataframe can handle both pt1 and pt2, download both, process and write all in one go