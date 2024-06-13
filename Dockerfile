FROM python:3.10.13

WORKDIR /artsort

COPY app/ .
COPY alembic.ini .
COPY migrations/ .
COPY requirements.txt .

RUN pip install -r requirements.txt
