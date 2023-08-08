"""
This example consumers messages from Memphis and prints them to the console.
"""

import argparse
import asyncio
import json
import os

from memphis import Memphis, MemphisConnectError, MemphisError, MemphisHeaderError

from zakar.config import MemphisCredentials


async def main(host, username, password, account_id):
    try:
        memphis = Memphis()
        await memphis.connect(
            host=host, username=username, password=password, account_id=account_id
        )
    except MemphisConnectError as e:
        print(e)
    asyncio.create_task(consume(memphis, station_name))


async def consume(memphis, station_name):
    try:
        consumer = await memphis.consumer(
            station_name=station_name, consumer_name=f"{station_name}_consumer"
        )

        while True:
            batch = await consumer.fetch()
            if batch is not None:
                for msg in batch:
                    serialized_record = msg.get_data()
                    record = json.loads(serialized_record)
                    print(record)
                    await msg.ack()

    except (MemphisError, MemphisConnectError) as e:
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

    return parser.parse_args()


if __name__ == "__main__":
    # args = parse_args()

    credentials = MemphisCredentials()
    asyncio.run(
        main(
            host=credentials.HOST,
            username=credentials.USERNAME,
            password=credentials.PASSWORD,
            account_id=credentials.ACCOUNT_ID,
        )
    )
