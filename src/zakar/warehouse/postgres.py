from pathlib import Path

import psycopg2
from psycopg2 import OperationalError
from psycopg2.extensions import connection


def execute_all_sql_files(connection: connection, directory: Path):
    for sql_file in directory.iterdir():
        execute_sql_file(connection=connection, sql_file=sql_file)


def execute_sql_file(
    connection: connection, sql_file: Path, parameters: dict[str, str | int] = {}
):
    with open(sql_file) as cmd:
        execute_sql(connection=connection, command=cmd.read(), parameters=parameters)


def execute_sql(
    connection: connection, command: str, parameters: dict[str, str | int] = {}
):
    with connection:
        with connection.cursor() as cur:
            try:
                cur.execute(command, parameters)
            except OperationalError as e:
                print(f"Encountered {e} when trying to run SQL command.")


def get_postgres_connection(
    host: str,
    port: int,
    database: str,
    user: str,
    password: str,
):
    try:
        con = psycopg2.connect(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password,
        )
    except (Exception, psycopg2.DatabaseError) as e:
        print(e)
    return con
