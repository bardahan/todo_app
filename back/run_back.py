from app import app as back_app

if __name__ == "__main__":
    back_app.run(debug=True, host="0.0.0.0", port=8001)
