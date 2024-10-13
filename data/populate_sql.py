import csv
import sqlite3

from data_extractor import extract
from sql_tables import TABLE_COLUMNS, CREATE_TABLES

connexion = sqlite3.connect("./database/data.db")
cursor = connexion.cursor()

print("Création des tables...")
for sql_command in CREATE_TABLES.values():
    cursor.execute(sql_command)



print(f"\nExtraction des données...")

tables_data = extract("./orders.csv")


for table_name, data in tables_data.items():
        print(f"{table_name} : {len(data)} entrées.")

print(f"\nPeuplement de la BDD...")

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

print(f"{inserted} lignes insérées avec {errors} erreurs.")


