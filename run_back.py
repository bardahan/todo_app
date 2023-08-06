import socket

from back.app import app as back_app

if __name__ == "__main__":
    back_app.run(debug=True, host=socket.gethostbyname(socket.gethostname()), port=8001)
