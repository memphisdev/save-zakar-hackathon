import asyncio
import json

from memphis import Memphis, MemphisConnectError, MemphisError

from config import MemphisCredentials


async def main(host, username, password, account_id):
    try:
        memphis = Memphis()
        await memphis.connect(
            host=host, username=username, password=password, account_id=account_id
        )

        consumer = await memphis.consumer(
            station_name="zakar-tweets", consumer_name="printing-consumer"
        )

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
