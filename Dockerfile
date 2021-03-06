FROM praekeltfoundation/django-bootstrap:py3.6

COPY . /app
WORKDIR /app

RUN pip install -e .

ENV DJANGO_SETTINGS_MODULE config.settings.production

RUN SECRET_KEY=collectstatic-key ALLOWED_HOSTS=placeholder RAPIDPRO_API_KEY=placeholder python manage.py collectstatic --noinput

CMD ["config.wsgi:application", "--timeout", "1800"]
