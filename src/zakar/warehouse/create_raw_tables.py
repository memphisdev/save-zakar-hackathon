from pathlib import Path

from zakar.config import PostgresConnectionInfo
from zakar.warehouse import execute_all_sql_files, get_postgres_connection


def main() -> None:
    pg_info = PostgresConnectionInfo()
    con = get_postgres_connection(
        host=pg_info.HOST,
        port=pg_info.PORT,
        database=pg_info.DATABASE_NAME,
        user=pg_info.USER,
        password=pg_info.PASSWORD,
    )

    create_tables_dir_path = Path(__file__).parent / "DDL/create_tables"
    print("\n=========================================================================")
    print(
        "Creating tables with DDL commands given in "
        f"{create_tables_dir_path.relative_to(create_tables_dir_path.parents[3])}."
    )
    print("=========================================================================\n")
    execute_all_sql_files(connection=con, directory=create_tables_dir_path)
    print("\n=========================================================================")
    print("Succesfully created all tables, if they did not already exist!")
    print("=========================================================================\n")
    con.close()


if __name__ == "__main__":
    main()
