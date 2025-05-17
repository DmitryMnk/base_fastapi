FROM python:3.13.3-alpine3.21


ARG USER_ID='1000'
ARG USER_ID=${USER_ID}
ENV USER_ID ${USER_ID}

ARG GROUP_ID='1000'
ARG GROUP_ID=${GROUP_ID}
ENV GROUP_ID ${GROUP_ID}

ARG POETRY_VIRTUALENVS_CREATE='false'
ARG POETRY_VIRTUALENVS_CREATE=$POETRY_VIRTUALENVS_CREATE
ENV POETRY_VIRTUALENVS_CREATE=$POETRY_VIRTUALENVS_CREATE


COPY ./pyproject.toml  .

RUN pip install -U pip
RUN pip install poetry
RUN poetry install --no-root


RUN apk add --no-cache shadow

RUN adduser -u $USER_ID -G www-data -s /bin/sh -D www-data || true
RUN mkdir /app && chown www-data:www-data /app
USER www-data

WORKDIR /app
