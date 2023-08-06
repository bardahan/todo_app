import socket

from web.app import app as web_app

if __name__ == "__main__":
    web_app.run(debug=True, host=socket.gethostbyname(socket.gethostname()), port=8000)
