FROM alpine:3.15

VOLUME /var/log/scraper

WORKDIR /usr/app/src

COPY . .

RUN apk add gcc g++ python3 python3-dev unixodbc unixodbc-dev py3-pip gnupg curl

RUN pip install --upgrade pip setuptools wheel

RUN pip install -r requirements.txt

ENV ENV_TYPE PROD

# Add SQL Server ODBC Driver 17 for Ubuntu 18.04
RUN chmod +x /usr/app/src/install_odbc.sh
RUN /usr/app/src/install_odbc.sh

#run the app
RUN python3 /usr/app/src/cns.py
CMD ["sh"]