"""
This example consumers messages from Memphis and prints them to the console.
"""

import asyncio
import json
import os

from memphis import Memphis, MemphisConnectError, MemphisError, MemphisHeaderError

from zakar.config import ConsumerConfig, MemphisCredentials


async def main(host, username, password, account_id, station_name="test"):
    try:
        memphis = Memphis()
        await memphis.connect(
            host=host, username=username, password=password, account_id=account_id
        )
        memphis = await fetch_records(memphis, station_name, consumer_name)

    except (MemphisError, MemphisConnectError) as e:
        print(e)

    finally:
        await memphis.close()


async def fetch_records(memphis, station_name, consumer_name):
    consumer = await memphis.consumer(
        station_name=station_name, consumer_name=consumer_name
    )

    records = []
    while True:
        batch = await consumer.fetch()
        if batch is not None:
            records += batch
            process_msgs(batch)
    return records


def process_msgs(batch):
    for msg in batch:
        serialized_record = msg.get_data()
        record = json.loads(serialized_record)
        print(record)


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
