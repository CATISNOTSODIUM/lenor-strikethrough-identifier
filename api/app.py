from flask import Flask, Response, jsonify, request
from rq import Queue
from .errors import errors
from .validate import validate_coordinates
from .utils import background_handler
import logging
app = Flask(__name__)

app.register_blueprint(errors)


@app.route("/")
def index():
    return Response("Welcome to remarkably-strike-identifier route", status=200)

@app.route("/upload", methods=['POST'])
def upload_image_and_coordinates():
    try:
        # validate fields
        if 'image' not in request.files:
            raise Exception("The field `image` is missing.")
        
        image = request.files['image'] 
        coordinates = validate_coordinates(request.form['coordinates'])
        n_original = len(coordinates)
        
        processed_coordinates = background_handler(image, coordinates) # Handling task
        n_processed = len(processed_coordinates)
        message = f"Successfully processed image. Before {n_original} After {n_processed}"
        logging.info(message)
        return jsonify(message=message, data = processed_coordinates, statusCode = 200), 200
    
    except Exception as e:
        logging.info(f'⚠️  {e}')
        return jsonify(message=f"Error {e}", statusCode = 500), 500
