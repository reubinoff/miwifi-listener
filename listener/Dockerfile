FROM python:3.9-slim

ARG USER=listener
ARG WORKDIR=/app/

WORKDIR $WORKDIR

RUN groupadd -f -g 1000 $USER && useradd -m $USER --gid 1000 && chown -R $USER:$USER $WORKDIR

# Install Poetry
RUN apt-get update
RUN apt-get install -y curl

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

# Copy using poetry.lock* in case it doesn't exist yet
COPY --chown=$USER:$USER ./pyproject.toml ./poetry.lock* $WORKDIR

RUN poetry install --no-root --no-dev

COPY --chown=$USER:$USER ./src/listener $WORKDIR

RUN apt-get clean && apt-get autoclean

CMD ["poetry","run", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80"]