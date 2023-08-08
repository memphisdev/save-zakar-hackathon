"""
This example consumers messages from Memphis and prints them to the console.
"""

import asyncio
import json
import os
import time

import pandas as pd
from memphis import Memphis, MemphisConnectError, MemphisError, MemphisHeaderError

from zakar.config import ConsumerConfig, MemphisCredentials

stations = ["zakar-tweets", "zakar-temperature-readings"]


async def main(
    host,
    username,
    password,
    account_id,
):
    try:
        memphis = Memphis()
        await memphis.connect(
            host=host, username=username, password=password, account_id=account_id
        )
        for name in stations:
            consumer = await memphis.consumer(
                station_name=name, consumer_name=f"{name}-consumer"
            )
            await consumer.destroy()
        tweet_consumer = await memphis.consumer(
            station_name=stations[0], consumer_name=f"{stations[0]}-consumer"
        )
        temp_consumer = await memphis.consumer(
            station_name=stations[1], consumer_name=f"{stations[1]}-consumer"
        )
        day = 1
        while True:
            print(day)
            (tweets, day), (temp, _) = await asyncio.gather(
                fetch_records(tweet_consumer, day), fetch_records(temp_consumer, day)
            )
            print(f"FINISHED FOR {day}")
            # day += 1
            await early_alert_system(temp, tweets)

    except (MemphisError, MemphisConnectError) as e:
        print(e)

    finally:
        await memphis.close()


async def early_alert_system(
    temperature_readings: list[dict[str, str | int]],
    tweets: list[dict[str, str | int]],
):
    print(len(temperature_readings))
    print(len(tweets))
    print()


async def fetch_records(consumer, day):
    records = []
    while True:
        batch = await consumer.fetch(batch_size=1)
        if batch is not None:
            for msg in batch:
                serialized_record = msg.get_data()
                record = json.loads(serialized_record)
                if record["day"] > day:
                    return records, record["day"]
                records.append(record)
                await msg.ack()


# async def process_msgs(batch, station_name):
#     # global combined_stations
#     global day
#     global stations
#     records = []
#     for msg in batch:
#         serialized_record = msg.get_data()
#         record = json.loads(serialized_record)
#         stations[station_name].append(record)
#         if day == 0:
#             day = record["day"]
#         if record["day"] > day:
#             print(station_name)
#             print(stations[station_name][0])
#             time.sleep(3)
#             # combined_stations = combined_stations.query(f"day != {day}")
#             day = record["day"]
#             stations[station_name] = []
#             return records
#         records.append(record)
#         await msg.ack()


combined_stations = pd.DataFrame(
    columns=["day", "geospatial_x", "geospatial_y", "temperature", "tweet"]
)

if __name__ == "__main__":
    credentials = MemphisCredentials()
    asyncio.run(
        main(
            host=credentials.HOST,
            username=credentials.USERNAME,
            password=credentials.PASSWORD,
            account_id=credentials.ACCOUNT_ID,
        )
    )
