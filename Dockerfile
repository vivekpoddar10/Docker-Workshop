# base image on which we will build on
FROM python:3.13.11-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# create a directory in image
WORKDIR /code

# copy dependency
COPY pyproject.toml uv.lock ./

# install dependency
RUN uv sync --locked

# copy application code
COPY main.py .

ENTRYPOINT [ "/code/.venv/bin/python", "main.py" ]
