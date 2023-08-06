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

    truncate_tables_dir_path = Path(__file__).parent / "DDL/truncate_tables"
    print("\n" + 100 * "=")
    print(
        "Truncating tables with DDL commands given in "
        f"{truncate_tables_dir_path.relative_to(truncate_tables_dir_path.parents[3])}."
    )
    print("\n" + 100 * "=")
    execute_all_sql_files(connection=con, directory=truncate_tables_dir_path)
    print("\n" + 100 * "=")
    print("Succesfully truncated all tables!")
    print("=========================================================================\n")
    con.close()


if __name__ == "__main__":
    main()
