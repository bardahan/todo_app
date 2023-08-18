from contextlib import contextmanager
import socket
import secrets

import psycopg2
from flask_cors import CORS

from datetime import datetime
from flask import Flask, jsonify

import back.settings as settings

app = Flask(__name__)
CORS(app)
app.secret_key = secrets.token_urlsafe(32)

connection = psycopg2.connect(
    database=settings.DB_SCHEME,
    user=settings.DB_USER,
    password=settings.DB_PASS,
    host=settings.DB_HOST,
    port="5432",
)


@contextmanager
def get_db_connection():
    connection = psycopg2.connect(
        database=settings.DB_SCHEME,
        user=settings.DB_USER,
        password=settings.DB_PASS,
        host=settings.DB_HOST,
        port="5432",
    )    
    try:
        yield connection
    finally:
        connection.commit()
        connection.close()


class SimpleResponse(object):
    OK_RESPONSE = dict(success=1)


def currentDate():
    return datetime.now().strftime("%d.%m.%y")


def currentTime():
    return datetime.now().strftime("%H:%M")


@app.route("/")
def index():
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("select * from todos")
            todos = cursor.fetchall()

    return jsonify(todos)


@app.route("/add/<todo>")
def add(todo):
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "insert into todos(todo,date,time) values(%s, %s, %s)",
                (todo, currentDate(), currentTime()),
            )
    return jsonify(SimpleResponse.OK_RESPONSE)


@app.route("/check/<int:id>")
def check(id):
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(f"update todos set status = 'True' where id = {id}")
    return jsonify(SimpleResponse.OK_RESPONSE)


@app.route("/uncheck/<int:id>")
def uncheck(id):
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(f"update todos set status = 'False' where id = {id}")
    return jsonify(SimpleResponse.OK_RESPONSE)


@app.route("/edit/<int:id>/<todo>")
def edit(id, todo):
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(f"update todos set todo = '{todo}' where id = {id}")
    return jsonify(SimpleResponse.OK_RESPONSE)


@app.route("/delete/<int:id>")
def delete(id):
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(f"delete from todos where id = {id}")
            cursor.execute(f"select setval('todos_id_seq',(select max(id) from todos))")
    return jsonify(SimpleResponse.OK_RESPONSE)


if __name__ == "__main__":
    app.run(debug=True, host=socket.gethostbyname(socket.gethostname()), port=8001)
