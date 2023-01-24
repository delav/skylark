version: "3.9"

services:

  redis:
    container_name: v_redis
    image: redis:alpine
    restart: always

  db:
    container_name: v_db
    image: postgres
    volumes:
      - ./data/db:/var/lib/postgresql/data
    env_file:
      - ./production.env
    restart: always

  web:
    container_name: v_web
    build: .
    command: bash -c "python manage.py makemigrations && python manage.py migrate && python manage.py collectstatic --no-input && gunicorn notification.wsgi:application --limit-request-line 0 --workers=4 --threads=4 --worker-class=gthread --bind 0.0.0.0:8000"
    env_file:
      - ./production.env
    volumes:
      - .:/app
      - ./staticfiles:/staticfiles
    expose:
      - 8000
    depends_on:
      - db
      - redis
    restart: always
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/"]
      interval: 30s
      timeout: 10s
      retries: 5

  celery:
    container_name: v_celery
    build: .
    command: celery -A notification worker -l info --concurrency 4
    env_file:
      - ./production.env
    # volumes:
    #   - ./redis/:/usr/src/app/
    depends_on:
      web:
        condition: service_healthy
      redis:
        condition: service_started
    restart: always


  celery-beat:
    container_name: v_celery_beat
    build: .
    command: celery -A notification beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler
    env_file:
      - ./production.env
    # volumes:
    #   - ./redis/:/usr/src/app/
    depends_on:
      - redis
    restart: always

  flower:
    container_name: v_celery_flower
    image: mher/flower
    command: celery flower
    environment:
      - CELERY_BROKER_URL=redis://redis:6379/0
      - FLOWER_PORT=5555
    ports:
      - 5555:5555
    depends_on:
      - redis
    restart: always

  nginx:
    container_name: v_nginx
    build: ./nginx
    volumes:
      - ./staticfiles:/staticfiles
      # - ./nginx/nginx.conf:/etc/nginx/nginx.conf
    ports:
      - 80:80
      - 443:443
    depends_on:
      - web
    restart: always
