FROM python:3.6

RUN python3 --version
RUN pip3 --version

RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /usr/src/parsing_kviz

ENV TZ Europe/Moscow
COPY . .

CMD
