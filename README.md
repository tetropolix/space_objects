# space-objects

**Docker image** - https://hub.docker.com/r/tetropolix/space_objects 

**Local usage**

**Dependencies installation**

*pip install -r requirements.txt*
-------------
1. Specify API_KEY configuration variable via **config.py** file or via **env variable**
    **config.py** option
    1. create **instance** folder in the root of the project (next to the flaskr dir)
    2. create **config.py** inside newly created folder
    3. assign your *api key* value to the **API_KEY** variable 
2. run **gunicorn -w 4 'flaskr:create_app()'** w flag is optional and it specifies the number of processes to run (default is 1)
