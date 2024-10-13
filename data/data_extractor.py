import csv

def extract(csv_path):
    tables_data = {
        "customer": {},
        "product": {},
        "customer_order": {},
        "order_detail": {}
    }

    with open(csv_path, newline='') as f:
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
