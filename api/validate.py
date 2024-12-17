import json
def validate_coordinates(coordinates):
    coordinates = json.loads(coordinates)
    # rough check
    first_coordinates_key = next(iter(coordinates))
    first_coordinates = coordinates[first_coordinates_key]
    first_x = first_coordinates[0]['x']
    first_y = first_coordinates[0]['y']
    return coordinates