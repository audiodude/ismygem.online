import flask

app = flask.Flask(__name__, static_folder='../frontend/dist')


@app.route('/')
def index():
  return app.send_static_file('index.html')


@app.route('/<path:filename>')
def send_static(filename):
  return app.send_static_file(filename)
