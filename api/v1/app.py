#!/usr/bin/python3
"""Principal API"""
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv


app = Flask(__name__)

# Register the app_views blueprint
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(ctx):
    """If the program finish"""
    storage.close()


# Define a custom 404 error handler
@app.errorhandler(404)
def handle_404(e):
    """Handling 404 error"""
    return jsonify(error="Not found"), 404


if __name__ == "__main__":
    app.run(
        host=getenv('HBNB_API_HOST', '0.0.0.0'),
        port=getenv('HBNB_API_PORT', 5000),
        threaded=True
    )
