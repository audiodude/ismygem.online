import json

import flask

from server.connection import check
from server.db import get_db
from server.models.schedule import Schedule


def has_db(name):
  return hasattr(flask.g, 'database')


def get_db(name):
  if not has_db(name):
    setattr(flask.g, 'database', get_db())
  return getattr(flask.g, 'database')


def validate_schedule_post(data):
  message = None
  if not data:
    message = 'A JSON payload is required'
  elif 'email' not in data:
    message = 'The field `email` is required'
  elif 'url' not in data:
    message = 'The field `url` is required'
  elif 'every_secs' not in data:
    message = 'The field `every_secs` is required'

  if message is not None:
    return flask.jsonify({'status': 400, 'message': message}), 400
  return None


def create_app():
  app = flask.Flask(__name__, static_folder='../frontend/dist')

  @app.route('/api/v1/check', methods=['POST'])
  def check_url():
    data = flask.request.get_json()
    if not data or not 'url' in data:
      return flask.jsonify({'status': 400, 'message': 'URL is required'}), 400

    result, message = check(data['url'])
    return flask.jsonify({'result': result, 'message': message})

  @app.route('/api/v1/schedule', methods=['POST'])
  def create_schedule():
    data = flask.request.get_json()
    resp = validate_schedule_post(data)
    if resp:
      return resp

    schedule = Schedule(get_db())
    schedule.insert_schedule(**data)

    return ('NO CONTENT', 204)

  @app.route('/')
  def index():
    return app.send_static_file('index.html')

  @app.route('/<path:filename>')
  def send_static(filename):
    return app.send_static_file(filename)

  return app
