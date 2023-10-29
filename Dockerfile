FROM python:3.10-slim

WORKDIR /sweet-nothings

# Open up
RUN umask 0022

# Install deps
RUN apt -y update && apt -y upgrade && apt -y install ffmpeg curl build-essential llvm

# Install poetry
RUN curl -sSL 'https://install.python-poetry.org' | python3 -

# Copy source
COPY main.py ./
COPY poetry.lock ./
COPY pyproject.toml ./
COPY README.md ./
COPY LICENSE ./
COPY sweetnothings ./sweetnothings

# Install file
RUN /root/.local/bin/poetry install

ENTRYPOINT [ "python3", "-u", "main.py" ]
