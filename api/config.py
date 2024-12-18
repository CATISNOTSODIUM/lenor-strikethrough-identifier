import torch 

# configure your configuration from here
def load_config():
    config = {}
    config["is_dense"] = True # models.DENSE
    
    if torch.cuda.is_available():
        config["device"] = 'cuda'
    else:
        config["device"] = 'cpu'
    config["width"] = 512
    config["height"] = 128
    config["batch-size"] = 64
    return config
