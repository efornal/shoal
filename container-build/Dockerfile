
FROM python:2.7.18-slim-buster

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED 1

EXPOSE 8000

RUN apt-get -y update && \
    apt-get install -y libcairo2-dev libcairo2 python-cairo python-cairo-dev \
    pkg-config gettext libpq-dev libyaml-dev \
    libldap2-dev libsasl2-dev libjpeg-dev zlib1g-dev libgtk2.0-dev \
    libgirepository1.0-dev \
    procps python-apt python3-cairo python3-cairo-dev

RUN pip install --upgrade pip

RUN apt-get clean && apt-get autoremove

WORKDIR /srv/shoal

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY container-build/entrypoint.sh /
RUN chmod +x /entrypoint.sh

COPY . ./

ENTRYPOINT ["/entrypoint.sh"]

CMD ["gunicorn", "shoal.wsgi:application", "--bind",  ":8000"]

