import logging
from sqlalchemy import create_engine
from pipeline.ingest import icd10_mortality_rates_processor


def configure_logger():
    logger = logging.getLogger('pipeline')
    logger.setLevel(logging.DEBUG)

    # create file handler which logs even debug messages
    fh = logging.FileHandler('main.log')
    fh.setLevel(logging.DEBUG)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger


def main():
    logger = configure_logger()

    logger.info("Starting pipeline...")

    engine = create_engine('postgresql://postgres@localhost:37780/who')
    target_table = 'mortality_rates'
    icd10_mortality_rates_urls = ["https://www.who.int/healthinfo/statistics/Morticd10_part1.zip",
                                  "https://www.who.int/healthinfo/statistics/Morticd10_part2.zip"]
    for url in icd10_mortality_rates_urls:
        processed_icd10_data = icd10_mortality_rates_processor.run(url)
        logger.info(f"Writing data to {target_table} table...")
        processed_icd10_data.to_sql(target_table, con=engine, if_exists='append', index=False, method='multi')


if __name__ == "__main__":
    main()
