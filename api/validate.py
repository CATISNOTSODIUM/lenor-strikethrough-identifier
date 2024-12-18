import json
def validate_coordinates(coordinates):
    coordinates = json.loads(coordinates)
    # rough check
    first_x = coordinates[0][0]['x']
    first_y = coordinates[0][1]['y']
    return coordinates