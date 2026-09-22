"""Tienda: catalogue, orders and an admin panel."""
import os

from flask import Flask, abort, jsonify, request, session

from src import backup, db
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


@app.route("/debug/session")
def debug_session():
    # Left over from development: a guest session to try the shop quickly.
    session["user_id"] = 0
    session["role"] = "user"
    return {"ok": True}


@app.route("/profile", methods=["POST"])
def update_profile():
    if "user_id" not in session:
        abort(401)
    # Display name, theme and language are kept in the session.
    for key, value in request.form.items():
        session[key] = value
    return {"ok": True}


@app.route("/admin/backup", methods=["POST"])
def admin_backup():
    if session.get("role") != "admin":
        abort(403)
    return {"output": backup.make_backup(request.form["label"])}


@app.route("/orders/<order_id>")
def show_order(order_id):
    if "user_id" not in session:
        abort(401)
    return jsonify(db.order_for(int(order_id), session["user_id"]))


@app.route("/reviews/search")
def search_reviews():
    return jsonify(db.search_reviews(request.args.get("q", "")))


if __name__ == "__main__":
    raise SystemExit("secaudit lab: this application is not meant to be run")
