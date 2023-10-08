FROM python:latest

VOLUME /var/log/scraper

WORKDIR /usr/app/src

COPY . .

RUN pip install -r requirements.txt

ENV ENV_TYPE PROD

CMD ["bash"]