# chop images and save at @/local
import os
import logging
from PIL import Image
from .cyclegan import predict
import json
import datetime

local_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "local")

def get_path_base_name(pathname):
    return os.path.splitext(os.path.basename(pathname))[0]


def pad_image(img, ratio, target_width=400): # ratio w / h
    target_height = int(target_width / ratio)
    original_width, original_height = img.size
    width_ratio = target_width / original_width
    height_ratio = target_height / original_height
    scale_factor = min(width_ratio, height_ratio)
    new_width = int(original_width * scale_factor)
    new_height = int(original_height * scale_factor)
    resized_img = img.resize((new_width, new_height), Image.LANCZOS)
    padded_img = Image.new('RGB', (target_width, target_height), (255, 255, 255))
    paste_x = (target_width - new_width) // 2
    paste_y = (target_height - new_height) // 2
    padded_img.paste(resized_img, (paste_x, paste_y))
    return padded_img 

# should be parallelized
def chop_images(image, coordinates):
    dir_name = get_path_base_name(image.filename)
    input_image_path = save_image(image, dir_name)
    
    img = Image.open(input_image_path)
    output_path = os.path.join(local_path, dir_name, "chopped")
    os.makedirs(output_path, exist_ok=True) 
    order = 0
    for coordinate in coordinates:
        chopped_file_name = f"_{order}_.jpg"
        top_left = coordinate[0]
        bottom_right = coordinate[2]
        img_tmp = img.crop((top_left['x'], top_left['y'], bottom_right['x'], bottom_right['y']))
        img_tmp = pad_image(img_tmp, 4) # make image size consistent by adding padding
        img_tmp.save(os.path.join(output_path, chopped_file_name))
        order = order + 1
    return dir_name
    
def TimestampMillisec64():
    return str((datetime.datetime.utcnow() - datetime.datetime(1970, 1, 1)).total_seconds() * 1000) 

def save_image(image, dir_name):
    filename = image.filename
    input_path = os.path.join(local_path, dir_name)
    os.makedirs(input_path, exist_ok=True) 
    
    # append time to file dir
    original_image_dir = os.path.join(input_path, TimestampMillisec64() + '_' + filename)
    
    image.save(original_image_dir)
    return original_image_dir



# Main handler
def background_handler(image, coordinates):
    logging.info(f"Chopping image {image.filename} ✂️")
    dir_name = chop_images(image, coordinates)
    logging.info("Finished chopping images")
    logging.info("Start predicting 🤖")
    coordinates = predict(dir_name, coordinates)
    logging.info("Finish predicting 😁")       
    return coordinates