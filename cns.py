from datetime import date
import os
import logging
import argparse
import ast
from cns_common_functions import load_config
from cns_scraper import scrap
from cns_validator import validate_data
from cns_storage import store_data


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


def do_scrapping(config: dict) -> bool:
    data = scrap(config)
    validated_data = validate_data(data)
    store_data(validated_data, config)
    return True


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
