import csv
import sqlite3

from sqlalchemy import create_engine

from sql_tables import CREATE_TABLES
from orm_models import Base


def get_sqlite_engine():
    connexion = sqlite3.connect("./database/data.db")
    cursor = connexion.cursor()
    return connexion, cursor

def create_tables_with_sql(cursor):
    print("Création des tables...")
    for sql_command in CREATE_TABLES.values():
        cursor.execute(sql_command)

def get_orm_engine():
    print("Création de la BDD...")
    return create_engine('sqlite:///database/data.db')

def create_tables_with_orm(engine):
    print("Création des tables...")
    Base.metadata.create_all(engine)

def extract(csv_path):
    """
    Renvoie l'ensemble des données contenues dans un fichier CSV
    Entrées
        csv_path : chemin vers le fichier csv (type : str)
    Retours
        tables_data : données de l'ensemble des tables (type: dict)
        structure :
            {"customer": {customer_id: [customer_id, country],
                            customer_id: [customer_id, country],
                            customer_id: [customer_id, country],
                            etc.},
            "customer_order: {order_id: [order_id, invoice_nb, invoice_date, customer_id],
                            order_id: [order_id, invoice_nb, invoice_date, customer_id],
                            order_id: [order_id, invoice_nb, invoice_date, customer_id],
                            etc.},
            "order_detail": {order_detail_id: [order_detail_id, quantity, order_id, product_id],
                            order_detail_id: [order_detail_id, quantity, order_id, product_id],
                            order_detail_id: [order_detail_id, quantity, order_id, product_id],
                            etc.},
            "product": {product_id: [product_id, description, price],
                            product_id: [product_id, description, price],
                            product_id: [product_id, description, price],
                            etc.}}

    """
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
            # A chaque itération, row contient les données d'une ligne du fichier CSV sous forme de liste
            if row[3] not in tables_data["customer"]:
                tables_data["customer"][row[3]] = [row[3], row[4]]
            if row[7] not in tables_data["product"]:
                description = row[8].replace("'", " ").replace('"', '')
                tables_data["product"][row[7]] = [row[7], description, row[9]]
            if row[0] not in tables_data["customer_order"]:
                tables_data["customer_order"][row[0]] = [row[0], row[1], row[2], row[3]]
            if row[5] not in tables_data["order_detail"]:
                tables_data["order_detail"][row[5]] = [row[5], row[6], row[0], row[7]]
    
    return tables_data
