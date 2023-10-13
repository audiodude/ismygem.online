# ismygem.online
Source code for the site at [ismygem.online](https://ismygem.online), an uptime monitor for the Gemini protocol

## Development

Dependencies are managed with [pipenv](https://pipenv.pypa.io/en/latest/). Make sure you are using Python 3.11, then run:

```bash
pipenv install
```

It will create a virtual env for you automatically and install the dev and prod dependencies. If you need to run a command using the Python dependencies or a binary provided by one of the Python packages, prefix it with `pipenv run`:

```bash
pipenv run pytest
```

## Tests
Tests are written in Python `unittest` style, and executed using the `pytest` harness. They are located next to the file under test as a `foo_test.py` file. To run the tests:

```bash
pipenv run pytest
```

## Deployment

Deployment is done to [fly.io](https://fly.io/). Continuous deployment is triggered by pushing to the github repo ([https://github.com/audiodude/ismygem.online](https://github.com/audiodude/ismygem.online)), which will automatically trigger deployment of the [Celery](https://docs.celeryq.dev/en/stable/index.html) workers and the web app.

## Architecture

The backend is written as a Python [Flask](https://flask.palletsprojects.com/en/3.0.x/) app. The frontend is written in [Vue 3](https://vuejs.org/) using the options API, and bundled with [Vite](https://vitejs.dev/) using [create-vue](https://github.com/vuejs/create-vue). CSS is implemented with [Tailwind](https://tailwindcss.com/).

The (under development) periodic checking is done with Celery, using a [Redis](https://redis.io/) instance (provided by [Upstash](https://upstash.com/) and integrated into fly.io) as both the broker and backend.
