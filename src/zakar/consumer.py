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
from zakar.predictor import fire_prediction

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
        day = 43
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
    preds = fire_prediction(tweets=tweets, temperature_readings=temperature_readings)
    print(preds)


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
