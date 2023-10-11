import json

import flask

from server.connection import check


def create_app():
  app = flask.Flask(__name__, static_folder='../frontend/dist')

  @app.route('/api/v1/check', methods=['POST'])
  def check_url():
    data = flask.request.get_json()
    if not data or not 'url' in data:
      resp_json = json.dumps({'status': 400, 'message': 'URL is required'})
      resp = flask.Response(resp_json, mimetype='application/json')
      resp.status_code = 400
      return resp

    result, message = check(data['url'])
    return flask.jsonify({'result': result, 'message': message})

  @app.route('/')
  def index():
    return app.send_static_file('index.html')

  @app.route('/<path:filename>')
  def send_static(filename):
    return app.send_static_file(filename)

  return app
