# syntax = docker/dockerfile:1

ARG NODE_VERSION=18.18.0
FROM node:${NODE_VERSION}-slim as fe-build

WORKDIR /usr/src/app

# Throw-away build stage to reduce size of final image
FROM fe-build as build

# Install packages needed to build node modules
RUN apt-get update -qq && \
  apt-get install -y build-essential pkg-config python-is-python3

# Install node modules
COPY --link frontend/package.json frontend/yarn.lock frontend/
RUN yarn install --frozen-lockfile

# Copy application code
COPY --link frontend frontend

# Build frontend
WORKDIR /usr/src/app/frontend
# Use --production=false because we need the devDependencies to build
RUN yarn install --production=false --frozen-lockfile
RUN yarn build



FROM python:3.12

RUN pip install --no-cache-dir pipenv

# Python app
WORKDIR /usr/src
COPY ./Pipfile app/Pipfile
COPY ./Pipfile.lock app/Pipfile.lock

WORKDIR /usr/src/app
RUN pipenv install --system --deploy --ignore-pipfile

COPY . .
COPY --from=build /usr/src/app/frontend ./frontend

CMD ["gunicorn", "-b", "0.0.0.0", "server.app:create_app()"]
