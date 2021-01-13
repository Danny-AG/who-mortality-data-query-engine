import logging
import psycopg2
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
    processed_icd10_data = icd10_mortality_rates_processor.run()


if __name__ == "__main__":
    main()
