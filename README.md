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

## Types



## APIs

`Rectangle` is represented by the coordinates of all vertices.
```JSON
[
    { x: 130, y: 95 },
    { x: 249, y: 95 },
    { x: 249, y: 118 },
    { x: 130, y: 118 }
]
```

Do not forget to edit `api/config.py` to edit the `cyclegan.py` configuration.