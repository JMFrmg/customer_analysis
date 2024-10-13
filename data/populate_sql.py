import os
import csv
import sqlite3

from sql_tables import TABLE_COLUMNS, CREATE_TABLES

connexion = sqlite3.connect("./database/data.db")
cursor = connexion.cursor()

print("Création des tables...")
for sql_command in CREATE_TABLES.values():
    cursor.execute(sql_command)

tables_data = {
    "customer": {},
    "product": {},
    "customer_order": {},
    "order_detail": {}
}

print(f"\nExtraction des données...")

with open('./orders.csv', newline='') as f:
    reader = csv.reader(f, delimiter=';')
    reader.__next__()
    for row in reader:
        if row[2] not in tables_data["customer"]:
            tables_data["customer"][row[2]] = [row[2], row[3]]
        if row[6] not in tables_data["product"]:
            description = row[7].replace("'", " ").replace('"', '')
            tables_data["product"][row[6]] = [row[6], description, row[8]]
        if row[0] not in tables_data["customer_order"]:
            tables_data["customer_order"][row[0]] = [row[0], row[1], row[2]]
        if row[4] not in tables_data["order_detail"]:
            tables_data["order_detail"][row[4]] = [row[4], row[5], row[0], row[6]]


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


