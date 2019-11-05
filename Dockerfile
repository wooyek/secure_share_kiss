FROM ubuntu

MAINTAINER Janusz Skonieczny @wooyek
LABEL version="0.1"

EXPOSE 8000

ENV DJANGO_SETTINGS_MODULE=secure_share_kiss.settings \
    SECRET_KEY=unsafe-testing-key \
    BASE_URL=http://127.0.0.1:8000 \
    EMAIL_URL=smtp+tls://SMTP_Injection:?@smtp.sparkpostmail.com:587

RUN apt-get update && apt-get -y upgrade && \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone && \
    apt-get install -y locales && \
    locale-gen en_US.UTF-8 && \
    apt-get install -y git git-flow unzip nano wget sudo curl build-essential && \
    apt-get install -y python python-dev python-pip python-virtualenv \
    python3 python3-dev python3-pip python3-venv python-enchant \
    python3.6 python3.6-dev python3.6-venv \
    libproj-dev libfreexl-dev libgdal-dev && \
    python3 -m pip install pip -U && \
    pip3 install invoke

COPY . /app/
RUN chmod +x /app/bin/docker-entrypoint.sh && \
    pip3 install -r /app/requirements.txt -e /app/ -U

ENTRYPOINT ["/app/bin/docker-entrypoint.sh"]