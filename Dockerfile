FROM praekeltfoundation/django-bootstrap:py3.6

COPY . /app
WORKDIR /app

RUN pip install -e .

ENV DJANGO_SETTINGS_MODULE config.settings.production

CMD ["config.wsgi:application", "--timeout", "1800"]
