# Strikethrough Identification Backend

## Quick start
Install python libraries from `requirements.txt` or use `conda` to create your own virtual environment.
```bash
conda config --append channels pytorch        
conda create --name <your_env_name> --file cyclegan_requirements.txt
conda activate <your_env_name>
```
Start your redis server by executing `redis-server` and `rq worker`.
To start the backend server, execute
```bash
bash bin/run.sh
```
You can configure the port number from `wsgi.py`. The default port number is `8080`.
Do not forget to edit `api/config.py` to edit the `cyclegan.py` configuration.

You can use the pre-trained model `best_f1.pth` from the original repository https://github.com/RaphaelaHeil/strikethrough-removal-cyclegans (strikethrough_identification) and save in `api/model`.

## APIs
### `/upload`
There are many ways to perform `POST` request (such as `Postman`).
![alt text](image.png)