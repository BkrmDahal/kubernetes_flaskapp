FROM python:3-slim

EXPOSE 5000
COPY . /code
RUN pip install -r /code/requirements.txt
WORKDIR code

CMD ["python", "app.py"]