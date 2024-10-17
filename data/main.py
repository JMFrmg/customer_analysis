# Imports
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


if __name__ == "__main__": # Sécurité
        if not os.path.exists("./database"):  # Contrôle de l'existence du dossier database
                os.makedirs("./database")
    
        if os.path.exists("./database/data.db"):
                os.remove("./database/data.db")
        
        # Peuplement de la base de données avec le module sqlite3
        connexion, cursor = get_sqlite_engine()  # Création des objects connexion et cursor de sqlite
        create_tables_with_sql(cursor)
        tables_data = extract("./csv_data/orders.csv")  # Extraction des données

        for table_name, data in tables_data.items():
                # table_name : nom de la table
                # data : lignes de cette table
                print(f"{table_name} : {len(data)} entrées.")

        print(f"\nPeuplement de la BDD...")
        start_time = time.time()  # Temps pour le calcul de la performance
        inserted, errors = populate_with_sql(tables_data, connexion, cursor)  # On envoie les données dans la base de données sqlite avec la fonction populate_with_sql
        print(f"{inserted} lignes insérées en sql avec {errors} erreurs en {time.time()- start_time} secondes.")  # Affichage des résultats

        os.remove("./database/data.db")  # Suppression de la base de données

        # Peuplement de la base de données avec l'ORM SqlAlchemy
        engine = get_orm_engine()
        create_tables_with_orm(engine)

        start_time = time.time()  # Contrôle de la performance de l'insertion des données avec l'ORM SqlAlchemy
        inserted, errors = populate_with_orm(tables_data, engine)
        print(f"{inserted} lignes insérées avec {errors} erreurs {time.time()- start_time} secondes.")

