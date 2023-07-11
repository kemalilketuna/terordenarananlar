FROM python:alpine
RUN pip install --upgrade pip
RUN pip install requests
RUN pip install sqlalchemy
RUN pip install psycopg
COPY scraper.py .
COPY minio.py .
COPY database.py .
CMD ["python", "./main.py"]

