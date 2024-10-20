import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db


bp = Blueprint("dataviz", __name__, url_prefix='/')

def customer():
    db = get_db()
    customers = db.execute(
        "SELECT * FROM customer LIMIT 10"
    ).fetchall()

    return render_template("dataviz/customer.html")