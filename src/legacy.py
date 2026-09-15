"""The CSV export the old admin panel used."""
from src.db import connect


def export_table(table):
    return connect().execute("SELECT * FROM " + table).fetchall()
