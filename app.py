import socket
import secrets
import psycopg2

from datetime import datetime
from flask import Flask, render_template, redirect

app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(32)

connection = psycopg2.connect(
    database="postgres",
    user="postgres",
    password="0Password",
    host="database-1.c8gurtjlyvsf.eu-north-1.rds.amazonaws.com",
    port="5432",
)


def currentDate():
    return datetime.now().strftime("%d.%m.%y")


def currentTime():
    return datetime.now().strftime("%H:%M")


@app.route("/")
def index():
    cursor = connection.cursor()
    cursor.execute("select * from todos")
    todos = cursor.fetchall()
    return render_template("/index.html", todos=todos)


@app.route("/add/<todo>")
def add(todo):
    cursor = connection.cursor()
    cursor.execute("insert into todos(todo,date,time) values(%s, %s, %s)", (todo, currentDate(), currentTime()))
    connection.commit()
    return redirect("/")


@app.route("/check/<int:id>")
def check(id):
    cursor = connection.cursor()
    cursor.execute(f"update todos set status = 'True' where id = {id}")
    cursor.execute('update todos set "editDate" = %s where id = %s', (currentDate(), id))
    cursor.execute(f'update todos set "editTime" = %s where id = %s', (currentTime(), id))
    connection.commit()
    return redirect("/")


@app.route("/uncheck/<int:id>")
def uncheck(id):
    cursor = connection.cursor()
    cursor.execute(f"update todos set status = 'False' where id = {id}")
    connection.commit()
    return redirect("/")


@app.route("/edit/<int:id>/<todo>")
def edit(id, todo):
    cursor = connection.cursor()
    cursor.execute(f"update todos set todo = '{todo}' where id = {id}")
    connection.commit()
    return redirect("/")


@app.route("/delete/<int:id>")
def delete(id):
    cursor = connection.cursor()
    cursor.execute(f"delete from todos where id = {id}")
    cursor.execute(f"select setval('todos_id_seq',(select max(id) from todos))")
    connection.commit()
    return redirect("/")


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(
        debug=True,
        host=socket.gethostbyname(socket.gethostname()),
        port=8000
    )
