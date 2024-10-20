import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db


bp = Blueprint("dataviz", __name__, url_prefix="/dataviz")


@bp.route("/", methods=["GET"])
def home():
    db = get_db()
    rows = db.execute(
        f"""
        SELECT country, invoice_nb, invoice_date, description, price, quantity 
        FROM customer ta
        JOIN customer_order tb1 ON ta.id = tb1.customer_id
        JOIN order_detail tb2 ON tb1.id = tb2.order_id
        JOIN product tb3 ON tb2.product_id = tb3.id
        LIMIT 50
        """
    ).fetchall()
    print(rows)
    columns = []
    if rows:
        columns = rows[-1].keys()
        
    return render_template("dataviz/table.html", columns=columns, rows=rows)

@bp.route("/<table>", methods=["GET"])
def customer(table):
    db = get_db()
    rows = db.execute(
        f"SELECT * FROM {table} LIMIT 50"
    ).fetchall()
    print(rows)
    columns = []
    if rows:
        columns = rows[-1].keys()
    print(columns)
        
    return render_template("dataviz/table.html", columns=columns, rows=rows)

