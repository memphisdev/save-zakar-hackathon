"""
This example consumes messages from Memphis and deposits them into a
MongoDB collection.
"""

import asyncio
import json

from memphis import Memphis, MemphisConnectError, MemphisError
from psycopg2.extensions import connection
from tqdm import tqdm

from zakar.config import (
    DataName,
    MemphisCredentials,
    PostgresConnectionInfo,
    Producer,
    StationName,
)
from zakar.warehouse import execute_sql_file, get_postgres_connection


async def main(
    producer: Producer,
    host: str,
    username: str,
    password: str,
    account_id: int,
    postgres_connection: connection,
):
    try:
        memphis = Memphis()
        await memphis.connect(
            host=host, username=username, password=password, account_id=account_id
        )

        consumer = await memphis.consumer(
            station_name=producer.station_name, consumer_name="postgres"
        )

        while True:
            batch = await consumer.fetch()
            if batch is not None:
                for msg in tqdm(batch):
                    serialized_record = msg.get_data()
                    record = json.loads(serialized_record)
                    execute_sql_file(
                        postgres_connection, producer.insert_command_path, record
                    )
                    await msg.ack()

    except (MemphisError, MemphisConnectError) as e:
        print(e)

    finally:
        postgres_connection.close()
        await memphis.close()


if __name__ == "__main__":
    pg_info = PostgresConnectionInfo()
    pg_con = get_postgres_connection(
        host=pg_info.HOST,
        port=pg_info.PORT,
        database=pg_info.DATABASE_NAME,
        user=pg_info.USER,
        password=pg_info.PASSWORD,
    )
    credentials = MemphisCredentials()
    tweets = Producer(StationName.TWEETS, data_name=DataName.TWEETS)
    fire_alerts = Producer(StationName.FIRE_ALERTS, data_name=DataName.FIRE_ALERTS)
    temperature_readings = Producer(
        StationName.TEMPERATURE_READINGS, data_name=DataName.TEMPERATURE_READINGS
    )
    asyncio.run(
        main(
            producer=tweets,
            host=credentials.HOST,
            username=credentials.USERNAME,
            password=credentials.PASSWORD,
            account_id=credentials.ACCOUNT_ID,
            postgres_connection=pg_con,
        ),
        main(
            producer=fire_alerts,
            host=credentials.HOST,
            username=credentials.USERNAME,
            password=credentials.PASSWORD,
            account_id=credentials.ACCOUNT_ID,
            postgres_connection=pg_con,
        ),
        main(
            producer=temperature_readings,
            host=credentials.HOST,
            username=credentials.USERNAME,
            password=credentials.PASSWORD,
            account_id=credentials.ACCOUNT_ID,
            postgres_connection=pg_con,
        ),
    )
