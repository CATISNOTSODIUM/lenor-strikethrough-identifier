import os
import logging
from pathlib import Path
import numpy as np
import torch
from torchvision import models, transforms
from torch.utils.data import DataLoader
from PIL import Image, ImageOps

# load config
from .config import load_config

local_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "local")
default_model_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "model", "best_f1.pth")
IMAGE_EXTENSION = "*.jpg"

# modified from original repository
def load_model(is_dense = True, device = 'cpu', model_path = default_model_path):

    if is_dense:
        model = models.densenet121(progress=False, num_classes=2)
        # change densenet to single channel input:
        originalLayer = model.features.conv0
        model.features.conv0 = torch.nn.Conv2d(in_channels=1, out_channels=originalLayer.out_channels,
                                               kernel_size=originalLayer.kernel_size,
                                               stride=originalLayer.stride, padding=originalLayer.padding,
                                               dilation=originalLayer.dilation, groups=originalLayer.groups,
                                               bias=originalLayer.bias, padding_mode=originalLayer.padding_mode)
    else:
        model = models.resnet18(progress=False, num_classes=2)
        originalLayer = model.conv1
        # change resnet to single channel input:
        model.conv1 = torch.nn.Conv2d(in_channels=1, out_channels=originalLayer.out_channels,
                                      kernel_size=originalLayer.kernel_size,
                                      stride=originalLayer.stride, padding=originalLayer.padding,
                                      dilation=originalLayer.dilation, groups=originalLayer.groups,
                                      bias=originalLayer.bias, padding_mode=originalLayer.padding_mode)
        
    stateDict = torch.load(model_path, map_location=torch.device(device))
    if 'model_state_dict' in stateDict.keys():
        stateDict = stateDict['model_state_dict']

    model.load_state_dict(stateDict)
    model = model.to(device)
    return model


def load_dataset(dir_name): # from local
    return data
 
def get_number_from_chopped_path(x):
    return int(repr(x).split('_')[-2])

class DatasetHandler: # compatible with the original repository class `CleanStruckDataset`
    def __init__(self, dir_name, config):
        self.dir_name = dir_name
        self.data = []
        predict_dir = os.path.join(local_path, dir_name, "chopped")
        predict_files = list(Path(predict_dir).glob(IMAGE_EXTENSION))
        # sort input based on index
        predict_files = sorted(predict_files, key=get_number_from_chopped_path) 
        self.data.extend([(f, 0) for f in predict_files])
        self.count = len(self.data)
        self.width = config["width"]
        self.height = config["height"]
        
    def __len__(self):
        return self.count
    def __getitem__(self, index: int): #  Dict[str, Any]
        filename, clean = self.data[index]
        image = Image.open(filename).convert('RGB')
        image = transforms.Compose([
            ImageOps.invert,
            transforms.Resize((self.width, self.height)), 
            transforms.Grayscale(num_output_channels=1),
            transforms.ToTensor(), # convert to tensor
        ])(image) 
        return {
            "image": image,
            "path": str(filename.relative_to(filename.parents[1]))
        }


def predict(dir_name, coordinates):
    config = load_config()
    dataset = DatasetHandler(dir_name, config)

    dataset = DataLoader(dataset, batch_size=config["batch-size"], shuffle=False, num_workers=1)
    
    
    model = load_model(config["is_dense"], config["device"], default_model_path)
    device = config["device"]
    # predict
    model.eval()
    predictedLabels = []
    
    with torch.no_grad():
        for datapoints in dataset:
            image = datapoints["image"].to(device)
            paths = datapoints["path"]
            predicted = model(image)
            predicted = torch.nn.functional.softmax(predicted, dim=1)
            predicted = torch.max(predicted, dim=1).indices.cpu().numpy()
            predictedLabels.extend(predicted.tolist())
    
    # remove strikethrough words
    for idx in range(len(predictedLabels) - 1, 0, -1):
        if (predictedLabels[idx] == 0):
            del coordinates[idx] 

    return coordinates

