TABLE_COLUMNS = tables_columns = {
                    "customer": ["id", "country"],
                    "product": ["id", "description", "price"],
                    "customerOrder": ["id", "invoice_nb", "customer_id"],
                    "orderDetail": ["id", "quantity", "order_id", "product_id"]
                }

CREATE_TABLES = {"customer": """CREATE TABLE customer (
	                id INTEGER NOT NULL, 
	                country VARCHAR, 
	                PRIMARY KEY (id)
                );""",

                "customerOrder": """CREATE TABLE customerOrder (
                    id INTEGER NOT NULL, 
                    invoice_nb INTEGER, 
                    customer_id INTEGER, 
                    PRIMARY KEY (id), 
                    FOREIGN KEY(customer_id) REFERENCES customer (id)
                );""",

                "product": """CREATE TABLE product (
                    id INTEGER NOT NULL, 
                    description VARCHAR, 
                    price FLOAT, 
                    PRIMARY KEY (id)
                );""",

                "product": """CREATE TABLE product (
                    id INTEGER NOT NULL, 
                    description VARCHAR, 
                    price FLOAT, 
                    PRIMARY KEY (id)
                );"""

                }

