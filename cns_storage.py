import logging
import json
import time


def store_data(data: dict, config: dict) -> bool:
    """
    Function to store data
    :param data: data to store
    :param config: config
    :return: True if success, False otherwise
    """
    try:
        #print(data)
        time_idx = str(time.time())
        with open(f"data_{time_idx}.json", "w") as f:
            json.dump(data, f)

    except Exception as e:
        logging.error("Error while storing data: {}".format(e))
        raise
    return True
