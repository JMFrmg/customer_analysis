import sqlite3

from data_extractor import (create_tables_with_sql,
                            get_sqlite_engine,
                            extract)
from populate_sql import populate_with_sql


if __name__ == "__main__":
    connexion, cursor = get_sqlite_engine()
    create_tables_with_sql(cursor)
    tables_data = extract("./orders.csv")

    for table_name, data in tables_data.items():
            print(f"{table_name} : {len(data)} entrées.")

    print(f"\nPeuplement de la BDD...")
    inserted, errors = populate_with_sql(tables_data, connexion, cursor)
    print(f"{inserted} lignes insérées avec {errors} erreurs.")
