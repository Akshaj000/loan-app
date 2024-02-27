FROM python:3.9-slim as base

ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get -y upgrade && \
    pip install virtualenv && \
    virtualenv /venv

ENV PATH="/venv/bin:$PATH"

FROM base as builder

RUN apt-get update && apt-get -y install --no-install-recommends \
    libpq-dev \
    build-essential \
    libblas-dev \
    liblapack-dev \
    gfortran \
    pkg-config

WORKDIR /backend

COPY requirements.txt .

RUN /venv/bin/pip install --no-cache-dir -r requirements.txt \
    && /venv/bin/pip install psycopg2-binary --no-cache-dir

COPY . .

FROM base as packager

RUN apt-get -y install --no-install-recommends libpq-dev

RUN useradd backend \
    && mkdir /backend \
    && chown -R backend:backend /backend

USER backend
WORKDIR /backend

COPY --from=builder /venv /venv
COPY --from=builder /backend /backend

EXPOSE 8000
CMD gunicorn -b 0.0.0.0:8000 --log-level=error framework.wsgi