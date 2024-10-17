# Imports
from sqlalchemy.orm import Session

from sql_tables import TABLE_COLUMNS
from orm_models import ORM_MODELS


tables_columns = {
    "customer": ["id", "country"],
    "product": ["id", "description", "price"],
    "customer_order": ["id", "invoice_nb", "invoice_date", "customer_id"],
    "order_detail": ["id", "quantity", "order_id", "product_id"]
}


def populate_with_sql(tables_data, connexion, cursor):
    """
    Peuplement de la base de données sqlite avec le module sqlite3
    Entrées :
        tables_data
            description : l'ensemble des données par table
            type : dictionnaire
            structure : {table1: {id1 : [value1, value2, etc.], id2: [value1, value2, value3], etc.}, 
                            table2:  {id1 : [value1, value2, etc.], id2: [value1, value2, value3], etc.}, 
                            etc.}
        connexion
            description : objet connexion sqlite3
        cursor
            description : objet cursor sqlite3
    Retour :
        inserted
            description : nombre de lignes insérées en base de données
            type : int
        errors
            description : nombre de lignes n'ayant pas pu être insérées en raison d'une erreur
            type : int

    """
    errors = 0
    inserted = 0

    for table_name, data in tables_data.items(): # On boucle sur les tables
        for row_id, row_data in data.items():  # On boucle sur les lignes
            # Création de la requête SQL sous forme de chaîne de caractères
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


def populate_with_orm(tables_data, engine):
    """
    Peuplement de la base de données sqlite avec l'orm SqlAlchemy'
    Entrées :
        tables_data
            description : l'ensemble des données par table
            type : dictionnaire
            structure : {table1: {id1 : [value1, value2, etc.], id2: [value1, value2, value3], etc.}, 
                            table2:  {id1 : [value1, value2, etc.], id2: [value1, value2, value3], etc.}, 
                            etc.}
        connexion
            description : objet connexion sqlite3
        cursor
            description : objet cursor sqlite3
    Retour :
        inserted
            description : nombre de lignes insérées en base de données
            type : int
        errors
            description : nombre de lignes n'ayant pas pu être insérées en raison d'une erreur
            type : int

    """
    print(f"\nPeuplement de la BDD avec SqlAlchemy...")

    errors = 0
    inserted = 0

    for table_name, data in tables_data.items():  # On boucle sur le nom des tables
        with Session(engine) as session:  # Creation de l'objet Session de SqlAlchemy. Il va nous servir pour nous connecter à la base de données
            for row_id, row_data in data.items():  # On boucle sur les lignes
                # row_id : contient l'id de chaque ligne de la table
                # row_data : liste qui contient toutes les données de la ligne pour une table
                order_product = ORM_MODELS[table_name](**dict(zip(tables_columns[table_name], row_data)))
                try:
                    session.add(order_product)
                    inserted += 1
                except Exception as e:
                    print(row_id, row_data)
                    print(e)
                    errors += 1
            session.commit()
    
    return inserted, errors


