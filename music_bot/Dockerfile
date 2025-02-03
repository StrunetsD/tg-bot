FROM python:latest


WORKDIR /tg-bot


COPY ./music_bot/requirements.txt ./requirements.txt


RUN pip install --upgrade pip \
    && pip install -r requirements.txt


RUN apt-get update \
    && apt-get install -y ffmpeg \
    && apt-get clean


COPY ./core ./core
COPY ./music_bot ./music_bot


WORKDIR /tg-bot/music_bot

CMD ["python", "-m", "run"]