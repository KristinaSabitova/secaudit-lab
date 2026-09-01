"""Tienda: catalogue, orders and an admin panel."""
import os

from flask import Flask, abort, jsonify, request, session

from src import db
from src.auth import check_password

app = Flask(__name__)
app.secret_key = os.environ.get("SHOP_SECRET_KEY", "")


@app.route("/login", methods=["POST"])
def login():
    user = db.user_by_name(request.form["user"])
    if user is None or not check_password(user, request.form["password"]):
        return {"ok": False}, 401
    session["user_id"] = user["id"]
    session["role"] = user["role"]
    return {"ok": True}


@app.route("/products/search")
def search_products():
    return jsonify(db.search_products(request.args.get("q", "")))


if __name__ == "__main__":
    raise SystemExit("secaudit lab: this application is not meant to be run")
