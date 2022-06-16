FROM python:3.10

WORKDIR /usr/src/pybot

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY findareason/tosts.txt ./tosts.txt
COPY findareason/bot.py bot.py

CMD [ "python", "./bot.py" ]