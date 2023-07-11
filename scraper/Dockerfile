FROM python:alpine
RUN pip install --upgrade pip
RUN pip install requests
RUN pip install sqlalchemy
RUN pip install psycopg
COPY main.py .
COPY minio.py .
COPY database.py .
COPY public_policy.json .
CMD ["python", "./main.py"]

