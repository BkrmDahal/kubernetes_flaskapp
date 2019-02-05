FROM python:3-slim

COPY . /code
RUN pip install -r /code/requirements.txt
WORKDIR code

CMD ["bash", "runserver.sh"]
