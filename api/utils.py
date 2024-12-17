# chop images and save at @/local
import os
from PIL import Image
import json
local_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "local")

def get_path_base_name(pathname):
    return os.path.splitext(os.path.basename(pathname))[0]

def chop_images(image, coordinates):
    dir_name = get_path_base_name(image.filename)
    input_image_path = save_image(image, dir_name)
    
    img = Image.open(input_image_path)
    output_path = os.path.join(local_path, dir_name, "chopped")
    os.makedirs(output_path, exist_ok=True) 
    
    
    for key, coordinate in coordinates.items():
        key_parse = json.loads(key)
        key_x, key_y = key_parse
        chopped_file_name = f"x_{key_x}_y_{key_y}.jpg"
        top_left = coordinate[0]
        bottom_right = coordinate[2]
        img_tmp = img.crop((top_left['x'], top_left['y'], bottom_right['x'], bottom_right['y']))
        img_tmp.save(os.path.join(output_path, chopped_file_name))
    
    
def save_image(image, dir_name):
    filename = image.filename
    input_path = os.path.join(local_path, dir_name)
    os.makedirs(input_path, exist_ok=True) 
    
    original_image_dir = os.path.join(input_path, filename)
    image.save(original_image_dir)
    return original_image_dir


