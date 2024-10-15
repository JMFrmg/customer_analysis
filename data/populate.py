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


def populate_with_orm(tables_data, engine):
    print(f"\nPeuplement de la BDD avec SqlAlchemy...")

    errors = 0
    inserted = 0

    for table_name, data in tables_data.items():
        with Session(engine) as session:
            for row_id, row_data in data.items():
                #print(row_data)
                #print(tables_columns[table_name])
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


