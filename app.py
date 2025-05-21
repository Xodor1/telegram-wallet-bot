
from flask import Flask, send_from_directory
from wallet_bot import start_bot
import threading
import os

app = Flask(__name__, static_folder="miniapp")

@app.route("/")
def serve_index():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/<path:path>")
def serve_static(path):
    return send_from_directory(app.static_folder, path)

if __name__ == '__main__':
    threading.Thread(target=start_bot).start()
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
