import sqlite3
import time
import os

from data_extractor import (create_tables_with_sql,
                            create_tables_with_orm,
                            get_sqlite_engine,
                            get_orm_engine,
                            extract)
from populate import (populate_with_sql, 
                      populate_with_orm)


if __name__ == "__main__":
        if not os.path.exists("./database"):
                os.makedirs("./database")
    
        if os.path.exists("./database/data.db"):
                os.remove("./database/data.db")
    
        connexion, cursor = get_sqlite_engine()
        create_tables_with_sql(cursor)
        tables_data = extract("./csv_data/orders.csv")

        for table_name, data in tables_data.items():
                print(f"{table_name} : {len(data)} entrées.")

        print(f"\nPeuplement de la BDD...")
        start_time = time.time()
        inserted, errors = populate_with_sql(tables_data, connexion, cursor)
        print(f"{inserted} lignes insérées en sql avec {errors} erreurs en {time.time()- start_time} secondes.")

        os.remove("./database/data.db")

        engine = get_orm_engine()
        create_tables_with_orm(engine)

        start_time = time.time()
        inserted, errors = populate_with_orm(tables_data, engine)
        print(f"{inserted} lignes insérées avec {errors} erreurs {time.time()- start_time} secondes.")

