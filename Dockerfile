# https://gist.github.com/usr-ein/c42d98abca3cb4632ab0c2c6aff8c88a

FROM python:3.11-slim as python-base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    \
    POETRY_VERSION=1.4.2 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"


ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

FROM python-base as builder-base


RUN apt-get update \
    && apt-get install --no-install-recommends -y \
    curl \
    build-essential \
    locales \
    && sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen \
    && sed -i -e 's/# es_ES.UTF-8 UTF-8/es_ES.UTF-8 UTF-8/' /etc/locale.gen \
    && locale-gen

ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8
ENV LC_ALL en_US.UTF-8

RUN --mount=type=cache,target=/root/.cache \
    curl -sSL https://install.python-poetry.org | python3 -

WORKDIR $PYSETUP_PATH
COPY poetry.lock pyproject.toml ./

RUN --mount=type=cache,target=/root/.cache \
    poetry install --without=dev

FROM python-base as development

ENV FASTAPI_ENV=development

WORKDIR $PYSETUP_PATH

COPY --from=builder-base $POETRY_HOME $POETRY_HOME
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH

RUN --mount=type=cache,target=/root/.cache \
    poetry install --with=dev

WORKDIR /code

EXPOSE 8000

CMD ["uvicorn", "--reload", "app.main:app"]

FROM python-base as production

ENV FASTAPI_ENV=production

COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH

COPY ./app /code/app

COPY ./data /code/data

COPY ./docs /code/docs

COPy ./classes /code/classes

WORKDIR /code

CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "app.main:app", "-b", "0.0.0.0:8000"]