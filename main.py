import requests
import time
import json
import os

URL = os.environ["URL"]


while True:
    print("Started scraping...")
    response = requests.get(URL)
    print("Scraping done!")
    json_data = response.json()

    time_idx = time.time()
    with open(f"data_{time_idx}", "w") as f:
        json.dump(json_data, f)

    print(f"Saved to data_{time_idx}")
