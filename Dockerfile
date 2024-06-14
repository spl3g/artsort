FROM python:3.10.13

WORKDIR /code

COPY . /code/
ENV PATH="${PATH}:/code/clis"

RUN pip install -r requirements.txt
