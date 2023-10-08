import logging
from requests import get


def scrap(config: dict) -> dict:
    """
    Function to scrape data from url
    :param config:
    :return: scraped data
    """
    response = {}
    logging.info("Started scraping from url: " + config['URL'])
    try:
        response = get(config['URL'])
        if response.status_code == 200:
            return response.json()
        else:
            response = {}
            logging.error("Error while scraping: " + str(response.status_code))
    except Exception as e:
        logging.error("Error while scraping: " + str(e))
        pass
    finally:
        logging.info("Scraping done!")

    return response
