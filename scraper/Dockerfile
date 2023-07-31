FROM python:3.10-slim
RUN pip install --upgrade pip
RUN pip install requests
RUN pip install sqlalchemy
RUN pip install minio
RUN pip install psycopg[binary]
COPY main.py /scraper/
COPY minio_utils.py /scraper/
COPY database_utils.py /scraper/
COPY models.py /scraper/
COPY public_policy.json /scraper/

CMD ["python3", "scraper/main.py"]

