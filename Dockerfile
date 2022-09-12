# docker build -t shoal:latest .

FROM python:2.7.18-buster
#FROM python:3.3-slim
#FROM python:3.9-slim-bullseye
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED 1

RUN apt-get -y update
RUN apt-get -y upgrade

RUN apt-get install -y libcairo2-dev libcairo2 python-cairo python-cairo-dev \
   pkg-config gettext libpq-dev libyaml-dev \
   libldap2-dev libsasl2-dev libjpeg-dev zlib1g-dev libgtk2.0-dev \
   libgirepository1.0-dev \
   procps python-apt python3-cairo python3-cairo-dev

RUN pip install --upgrade pip
WORKDIR /srv/shoal
EXPOSE 8000

COPY app app
COPY shoal shoal
COPY LICENSE .
COPY locale locale
COPY manage.py .
COPY README.md .
COPY static static
COPY templates templates
COPY password_change password_change
COPY ldap_people ldap_people

COPY requirements.txt .
RUN pip install -r requirements.txt
RUN apt-get clean && apt-get autoremove

COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

CMD ["gunicorn", "shoal.wsgi:application", "--bind",  ":8000"]
