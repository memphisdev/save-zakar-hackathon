import argparse
import asyncio
from io import TextIOWrapper
import os
import urllib
import zipfile

from tqdm import tqdm

from memphis import (
    Memphis,
    Headers,
    MemphisError,
    MemphisConnectError,
    MemphisHeaderError,
    MemphisSchemaError,
)

STATIONS = {
    "tweets": "zakar-tweets",
    "temps": "zakar-temperature-readings",
    "alerts": "zakar-fire-alerts",
}

FLNAMES = {
    "tweets": "simulated-training-data/tweets.json",
    "temps": "simulated-training-data/temperature_readings.json",
    "alerts": "simulated-training-data/fire_alerts.json",
}

RETENTION_SEC = 2 * 7 * 24 * 60 * 60  # two weeks

DATA_URL = "https://memphis-public-files.s3.eu-central-1.amazonaws.com/wildfire-simulated-data/simulated-training-data.zip"


def line_reader(zipfl, flname):
    with zipfl.open(flname, "r") as fl:
        lines = [ln.strip() for ln in TextIOWrapper(fl, encoding="utf-8")]
        return lines


async def main(host, username, password, account_id, rate_limiting):
    try:
        print("Connecting to Memphis.")
        memphis = Memphis()
        await memphis.connect(
            host=host, username=username, password=password, account_id=account_id
        )

        print("Downloading data")
        local_flname, _ = urllib.request.urlretrieve(DATA_URL)
        print("Done.")
        print()

        print("Uploading data to Memphis.")
        with zipfile.ZipFile(local_flname) as zipfl:
            for data_type, flname in FLNAMES.items():
                station = STATIONS[data_type]

                print("Creating station {}".format(station))
                await memphis.station(station, retention_value=RETENTION_SEC)
                print()

                print("Extracting data")
                messages = line_reader(zipfl, flname)

                print("Uploading data.")
                messages = line_reader(zipfl, flname)
                producer = await memphis.producer(
                    station_name=station, producer_name="data-uploader"
                )

                if not rate_limiting:
                    for msg in tqdm(messages):
                        await producer.produce(
                            bytearray(msg, "utf-8"), async_produce=True
                        )
                else:
                    background_tasks = set()
                    for msg in tqdm(messages):
                        task = asyncio.create_task(
                            producer.produce(bytearray(msg, "utf-8"))
                        )
                        background_tasks.add(task)
                        task.add_done_callback(background_tasks.discard)

                        if len(background_tasks) >= 1000:
                            while len(background_tasks) >= 500:
                                await asyncio.sleep(0.1)
                print()

        print("Destroying producer.")
        await producer.destroy()

    except (
        MemphisError,
        MemphisConnectError,
        MemphisHeaderError,
        MemphisSchemaError,
    ) as e:
        print(e)

    finally:
        await memphis.close()


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--host", type=str, required=True, help="Memphis broker host")

    parser.add_argument("--username", type=str, required=True, help="Memphis username")

    parser.add_argument("--password", type=str, required=True, help="Memphis password")

    parser.add_argument(
        "--account-id", type=int, required=True, help="Memphis account ID"
    )

    parser.add_argument(
        "--enable-rate-limiting",
        action="store_true",
        help="Enable rate limiting to avoid timeout errors",
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    asyncio.run(
        main(
            args.host,
            args.username,
            args.password,
            args.account_id,
            args.enable_rate_limiting,
        )
    )
