from pathlib import Path

from zakar.config import PostgresConnectionInfo
from zakar.warehouse import execute_sql_all_files, get_postgres_connection


def main() -> None:
    pg_info = PostgresConnectionInfo()
    con = get_postgres_connection(
        host=pg_info.HOST,
        port=pg_info.PORT,
        database=pg_info.DATABASE_NAME,
        user=pg_info.USER,
        password=pg_info.PASSWORD,
    )
    # table_names = ["temperature_readings", "tweets", "fire_alerts"]

    create_tables_dir_path = Path(__file__).parent / "DDL/create_tables"
    execute_sql_all_files(connection=con, dir_path=create_tables_dir_path)
    con.close()


if __name__ == "__main__":
    main()
