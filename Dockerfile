FROM python:3.7.3-alpine

RUN mkdir -p /usr/src/dino-extinction
WORKDIR /usr/src/dino-extinction

COPY requirements.txt /usr/src/dino-extinction
RUN apk --update add --virtual build-dependencies libffi-dev openssl-dev python-dev py-pip build-base \
    && pip install --upgrade pip \
    && pip install -r requirements.txt \
    && apk del build-dependencies

COPY wsgi.py /usr/src/dino-extinction
COPY ascii.txt /usr/src/dino-extinction
COPY dino_extinction /usr/src/dino-extinction/dino_extinction

EXPOSE 8080

CMD ["python", "-u", "wsgi.py"]
