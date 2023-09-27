from flask import jsonify
from application import create_app

app = create_app()
@app.route("/")
def hello_interiordesign():
    return jsonify({
        "message": "Welcome to Interior Design API",
        "description": "Interior Design API",
        "endpoint": [
            "GET /"
        ]
    }), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0")
