from flask import Flask, Response, jsonify, request

from .errors import errors
from .validate import validate_coordinates
from .utils import chop_images
app = Flask(__name__)
app.register_blueprint(errors)


@app.route("/")
def index():
    return Response("Welcome to remarkably-strike-identifier route", status=200)

@app.route("/upload", methods=['POST'])
def upload_image_and_coordinates():
    try:
        image = request.files['image'] 
        coordinates = validate_coordinates(request.form['coordinates'])
        # todo: use redis queue for job handling
        chop_images(image, coordinates)
        return jsonify(message="Success", statusCode = 200), 200
    except Exception as e:
        return jsonify(message=f"Error {e}", statusCode = 500), 500
