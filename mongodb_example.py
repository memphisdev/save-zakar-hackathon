"""
This example consumes messages from Memphis and deposits them into a
MongoDB collection.
"""

import argparse
import asyncio
import json

from memphis import Memphis, MemphisError, MemphisConnectError

from pymongo import MongoClient

async def main(host, username, password, account_id, mongo_uri, mongo_database):
    client = MongoClient(mongo_uri)
    db = client[mongo_database]
    collection = db["zakar-tweets"]

    try:
        memphis = Memphis()
        await memphis.connect(host=host,
                              username=username,
                              password=password,
                              account_id = account_id)

        consumer = await memphis.consumer(station_name="zakar-tweets", consumer_name="mongodb-example")

        while True:
            batch = await consumer.fetch()
            if batch is not None:
                for msg in batch:
                    serialized_record = msg.get_data()
                    record = json.loads(serialized_record)
                    collection.insert_one(record)

    except (MemphisError, MemphisConnectError) as e:
        print(e)

    finally:
        client.close()
        await memphis.close()

def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--memphis-host",
                        type=str,
                        required=True,
                        help="Memphis broker host")

    parser.add_argument("--memphis-username",
                        type=str,
                        required=True,
                        help="Memphis username")

    parser.add_argument("--memphis-password",
                        type=str,
                        required=True,
                        help="Memphis password")

    parser.add_argument("--memphis-account-id",
                        type=int,
                        required=True,
                        help="Memphis account ID")

    parser.add_argument("--mongo-host",
                        type=str,
                        required=True,
                        help="MongoDB host")

    parser.add_argument("--mongo-username",
                        type=str,
                        required=True,
                        help="MongoDB username")

    parser.add_argument("--mongo-password",
                        type=str,
                        required=True,
                        help="MongoDB password")

    parser.add_argument("--mongo-database",
                        type=str,
                        required=True,
                        help="MongoDB database")

    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()

    db_uri = "mongodb://{}:{}@{}:27017/".format(args.mongo_host,
                                                args.mongo_username,
                                                args.mongo_password)

    asyncio.run(main(args.memphis_host,
                     args.memphis_username,
                     args.memphis_password,
                     args.memphis_account_id,
                     db_uri,
                     args.mongo_database))
