import csv
import sqlite3

from data_extractor import extract
from sql_tables import TABLE_COLUMNS, CREATE_TABLES



def populate_with_sql(tables_data, connexion, cursor):
    errors = 0
    inserted = 0

    for table_name, data in tables_data.items():
        for row_id, row_data in data.items():
            sql_command = f"""INSERT INTO {table_name} ('{"', '".join(TABLE_COLUMNS[table_name])}') VALUES ('{"', '".join(row_data)}')"""
            try:
                cursor.execute(sql_command)
                inserted += 1
            except Exception as e:
                print(sql_command)
                print(e)
                errors += 1
        connexion.commit()
    
    return (inserted, errors)


