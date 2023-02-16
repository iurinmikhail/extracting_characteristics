FROM python:3.10
WORKDIR ./
COPY ./requirements.txt ./requirements.txt
COPY . .
RUN pip install -r /requirements.txt
