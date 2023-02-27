FROM python:3.10-slim-bullseye
COPY . /src
WORKDIR /src
RUN pip install -r requirements.txt
EXPOSE 8000 
ENTRYPOINT ["gunicorn", "-w 4", "-b 0.0.0.0:8000", "flaskr:create_app()"]
