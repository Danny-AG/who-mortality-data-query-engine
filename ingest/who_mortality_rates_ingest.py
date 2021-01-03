import requests
import zipfile
import logging
from tqdm import tqdm


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
zipped_file_path = download_file(who_mortality_rates_url)

# Extract data
extracted_file_name = unzip_file(zipped_file_path)

# Read into dataframe

# Process dataframe

# Write dataframe to database

# If dataframe can handle both pt1 and pt2, download both, process and write all in one go