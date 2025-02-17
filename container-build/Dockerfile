
FROM python:2.7.18-slim-buster as base

ARG LOCAL_TIME=America/Argentina/Cordoba

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND=noninteractive

EXPOSE 8000
WORKDIR /srv/shoal

RUN rm /etc/localtime \
    && ln -s /usr/share/zoneinfo/$LOCAL_TIME /etc/localtime

RUN apt-get -y update && apt-get install -y --no-install-recommends \
    python-apt libcairo2 python-cairo  \
    pkg-config gettext procps \
    && apt-get clean && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir --upgrade pip

FROM base as builder

RUN apt-get -y update && apt-get install -y \
    apt-utils libcairo2-dev python-cairo-dev \
    libpq-dev libyaml-dev \
    libldap2-dev libsasl2-dev libjpeg-dev zlib1g-dev libgtk2.0-dev \
    libgirepository1.0-dev

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM base

COPY --from=builder /usr/local/lib/python2.7/site-packages /usr/local/lib/python2.7/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin


COPY container-build/entrypoint.sh /
RUN chmod +x /entrypoint.sh

COPY . ./

RUN mkdir -vp /srv/django_sessions

ENTRYPOINT ["/entrypoint.sh"]

CMD ["gunicorn", "shoal.wsgi:application", "--config", "gunicorn.conf.py"]

