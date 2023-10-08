FROM python:latest

WORKDIR /usr/app/src

COPY . .

RUN pip install -r requirements.txt

ENV URL="https://api.chucknorris.io/jokes/random"

CMD ["bash"]