from datetime import date
import os
import logging
import argparse
import ast
from cns_common_functions import load_config
from cns_scraper import scrap
from cns_validator import validate_data
import cns_storage
import pandas as pd

ENV_TYPE = os.environ["ENV_TYPE"]

'''
while True:
    print("Started scraping...")
    response = requests.get(URL)
    print("Scraping done!")
    json_data = response.json()

    time_idx = time.time()
    with open(f"data_{time_idx}", "w") as f:
        json.dump(json_data, f)

    print(f"Saved to data_{time_idx}")
'''


def do_scrapping(config: dict):
    data = scrap(config)
    valid_jokes, invalid_jokes = validate_data(data)
    df_valid_jokes = pd.DataFrame(valid_jokes)
    df_valid_jokes['categories'] = df_valid_jokes['categories'].apply(lambda x: str(x).replace('[', '').replace(']', ''))
    storage = cns_storage.jokes_storage(config)
    storage.add_valid_data(df_valid_jokes)
    if len(invalid_jokes)>0:
        storage.add_invalid_data(invalid_jokes)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Chuck Norris Scraper")
    parser.add_argument(
        "-cp",
        "--config_path",
        help="Path to config file. If not passed, script will try to load cns_config.json",
        required=False,
    )
    parser.add_argument(
        "-cd",
        "--config_dict",
        help="You can pass entries in {'key':'value'} format, which will OVERWRITE settings from loaded config file. "
             "Usefull for passing credentials.",
        required=False,
    )

    args = parser.parse_args()
    if args.config_path is not None:
        print("Loading config file: ", str(args.config_path))
        config = load_config(args.config_path)[ENV_TYPE]
    else:
        print("Loading default config")
        config = load_config("cns_config.ini")[ENV_TYPE]

    if args.config_dict is not None:
        for key, val in ast.literal_eval(args.config_dict).items():
            config[key] = val
            logging.info(
                "Overwriting: %s setting from config file with value: %s",
                str(key),
                str(val),
            )

    logging.basicConfig(
        filename=str(config['LOG_PATH'])+"cns_" + str(date.today()) + ".log",
        format="%(asctime)s:%(levelname)s:%(message)s",
        level=logging.DEBUG,
        force=True
    )

    do_scrapping(config)
