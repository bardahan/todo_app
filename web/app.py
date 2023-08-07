import socket
import secrets
import requests

from flask import Flask, render_template

from web.settings import API_BASE_URL

app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(32)


@app.route("/")
def index():
    res = requests.get(API_BASE_URL)
    todos = res.json()
    return render_template("/index.html", todos=todos, api_url=API_BASE_URL)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(
        debug=True,
        host=socket.gethostbyname(socket.gethostname()),
        port=8000
    )
