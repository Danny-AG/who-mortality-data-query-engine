import requests
import zipfile


def download_file(url):
    local_filename = url.split('/')[-1]
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return local_filename


def unzip_file(zip_file_path):
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall("./")
    return zip_ref.filename


# download pt1 of data
who_mortality_rates_url = "https://www.who.int/healthinfo/statistics/Morticd10_part1.zip"
zipped_file_path = download_file(who_mortality_rates_url)

# unzip data
extracted_file_path = unzip_file(zipped_file_path)

# Read into dataframe

# Process dataframe

# Write dataframe to database

# If dataframe can handle both pt1 and pt2, download both, process and write all in one go