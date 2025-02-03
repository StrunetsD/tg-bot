FROM python:latest

WORKDIR /tg-bot/admin


COPY ./admin/requirements.txt ./admin/requirements.txt


RUN pip install --upgrade pip \
    && pip install -r ./admin/requirements.txt


COPY ./admin ./admin
COPY ./core ./core
COPY ./database ./database




WORKDIR /tg-bot/admin


CMD ["python", "-m", "admin.app"]



