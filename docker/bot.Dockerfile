FROM python:3.12-alpine

WORKDIR "/app"

RUN apk add --no-cache \
    gcc \
    musl-dev \
    python3-dev \
    libffi-dev \
    gmp-dev \
    build-base \
    py3-pip \
    busybox-extras \
    curl

COPY /backend /app/backend
COPY /assets /app/assets
COPY /requirements.txt /app


RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt


RUN addgroup -S bot && adduser -S bot -G bot
USER bot



CMD ["python3", "-m", "backend.main", "--app", "bot"]