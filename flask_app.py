#!/usr/bin/env python
# vi: set syntax=python ts=4 sw=4 sts=4 et ff=unix ai si :

from flask import Flask, g, request, render_template
import sqlite3
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, 'lbdb.db')

SQL = """
    select book_title,auth_name  from v_search
    WHERE book_title LIKE ? OR auth_name LIKE ?
"""

def query_books(keyword):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(SQL,  (f'%{keyword}%', f'%{keyword}%'))
    results = cursor.fetchall()
    conn.close()

    return results

@app.route("/", methods=["GET", "POST"])
def search():
    results = []
    if request.method == "POST":
        keyword = request.form.get("keyword", "").strip()
        if keyword:
            results = query_books(keyword)
    return render_template("search.html", results=results)


@app.teardown_appcontext
def close_connection(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()

#if __name__ == "__main__":
#    app.run(host="0.0.0.0", port=81)
