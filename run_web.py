from web.app import app as web_app

if __name__ == "__main__":
    web_app.run(debug=True, host="0.0.0.0", port=8000)
