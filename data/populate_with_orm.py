import sqlite3
import csv

from sqlalchemy import insert, create_engine
from sqlalchemy.orm import Session

from orm_models import (Base, ORM_MODELS)


connexion = sqlite3.connect("./database/data.db")
cursor = connexion.cursor()

print("Création de la BDD...")
engine = create_engine('sqlite:///database/data.db')

print("Création des tables...")
Base.metadata.create_all(engine)

tables_data = {
    "customer": {},
    "product": {},
    "customer_order": {},
    "order_detail": {}
}

tables_columns = {
    "customer": ["id", "country"],
    "product": ["id", "description", "price"],
    "customer_order": ["id", "invoice_nb", "customer_id"],
    "order_detail": ["id", "quantity", "order_id", "product_id"]
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
    with Session(engine) as session:
        for row_id, row_data in data.items():
            order_product = ORM_MODELS[table_name](**dict(zip(tables_columns[table_name], row_data)))
            try:
                session.add(order_product)
                inserted += 1
            except Exception as e:
                print(row_id, row_data)
                print(e)
                errors += 1
        session.commit()

print(f"{inserted} lignes insérées avec {errors} erreurs.")
