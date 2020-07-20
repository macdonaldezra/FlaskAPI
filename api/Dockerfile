FROM python:3.8.1-slim-buster as builder

WORKDIR /usr/src/api

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

RUN apt-get update && apt-get install -y --no-install-recommends gcc
RUN pip install --upgrade pip
COPY . /usr/src/api/

# install Python dependencies
COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/api/wheels -r requirements.txt

# ********************
# * PRODUCTION STAGE *
# ********************
FROM python:3.8.1-slim-buster

RUN adduser --system quser
ENV HOME=/home/quser
WORKDIR $HOME

# Install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends netcat
COPY --from=builder /usr/src/api/wheels /wheels
COPY --from=builder /usr/src/api/requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache /wheels/*
COPY . $HOME

RUN chown -R quser:users $HOME
USER quser

EXPOSE 8080
ENTRYPOINT ["gunicorn"]
CMD ["--bind", "0.0.0.0:8080", "run:app"]