"""
This example consumers messages from Memphis and prints them to the console.
"""

import argparse
import asyncio
import json
import os

from memphis import Memphis, MemphisError, MemphisConnectError, MemphisHeaderError
        
async def main(host, username, password, account_id):
    try:
        memphis = Memphis()
        await memphis.connect(host=host,
                              username=username,
                              password=password,
                              account_id=account_id)
        
        consumer = await memphis.consumer(station_name="zakar-tweets", consumer_name="printing-consumer")

        while True:
            batch = await consumer.fetch()
            if batch is not None:
                for msg in batch:
                    serialized_record = msg.get_data()
                    record = json.loads(serialized_record)
                    print(record)
                    msg.ack()

    except (MemphisError, MemphisConnectError) as e:
        print(e)

    finally:
        await memphis.close()

def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--host",
                        type=str,
                        required=True,
                        help="Memphis broker host")

    parser.add_argument("--username",
                        type=str,
                        required=True,
                        help="Memphis username")

    parser.add_argument("--password",
                        type=str,
                        required=True,
                        help="Memphis password")

    parser.add_argument("--account-id",
                        type=int,
                        required=True,
                        help="Memphis account ID")

    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()

    asyncio.run(main(args.host, args.username, args.password, args.account_id))
