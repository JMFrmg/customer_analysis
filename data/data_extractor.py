import csv
import sqlite3

from sql_tables import TABLE_COLUMNS, CREATE_TABLES


def get_sqlite_engine():
    connexion = sqlite3.connect("./database/data.db")
    cursor = connexion.cursor()
    return connexion, cursor

def create_tables_with_sql(cursor):
    print("Création des tables...")
    for sql_command in CREATE_TABLES.values():
        cursor.execute(sql_command)

def extract(csv_path):
    tables_data = {
        "customer": {},
        "product": {},
        "customer_order": {},
        "order_detail": {}
    }

    with open(csv_path, newline='') as f:
        print(f"\nExtraction des données...")
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
    
    return tables_data
