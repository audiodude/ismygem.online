import json
from unittest.mock import patch

import pytest

from server.app import create_app, get_db
from server.db import db_test_fixture
from server.models.schedule import Schedule


class AppTest:

  @pytest.fixture
  def app(self):
    app = create_app()
    app.config['TESTING'] = True
    return app

  @pytest.fixture
  def db_test(self):
    yield from db_test_fixture()

  @patch('server.app.check')
  def test_check_url(self, mock_check, app):
    mock_check.return_value = (True, None)
    with app.test_client() as client:
      rv = client.post('/api/v1/check',
                       json={'url': 'gemini://foo.server.fake'})
      assert '200 OK' == rv.status
      assert {'result': True, 'message': None} == rv.get_json()

  @patch('server.app.check')
  def test_check_url_sends_back_msg(self, mock_check, app):
    mock_check.return_value = (False,
                               'Some kind of wacky error occured (NET_WACKY)')
    with app.test_client() as client:
      rv = client.post('/api/v1/check',
                       json={'url': 'gemini://foo.server.fake'})
      assert '200 OK' == rv.status
      assert {
          'result': False,
          'message': 'Some kind of wacky error occured (NET_WACKY)'
      } == rv.get_json()

  @patch('server.app.check')
  def test_check_url_no_json(self, mock_check, app):
    mock_check.return_value = (True, None)
    with app.test_client() as client:
      rv = client.post('/api/v1/check')
      assert '415 UNSUPPORTED MEDIA TYPE' == rv.status

  @patch('server.app.check')
  def test_check_url_no_url(self, mock_check, app):
    mock_check.return_value = (True, None)
    with app.test_client() as client:
      rv = client.post('/api/v1/check', json={'foo': 'bar'})
      assert '400 BAD REQUEST' == rv.status

  @patch('server.app.get_db')
  @patch('server.worker.send_verification_email')
  def test_create_schedule(self, mock_send_verify_email, mock_get_db, app,
                           db_test):
    mock_get_db.return_value = db_test

    with app.test_client() as client:
      rv = client.post('/api/v1/schedule',
                       json={
                           'email': 'foo@bar.fake',
                           'url': 'gemini://foo.server.fake',
                           'every_secs': 60
                       })
      mock_send_verify_email.delay.assert_called_once()
      assert '204 NO CONTENT' == rv.status

  @patch('server.app.get_db')
  def test_create_schedule_missing_email(self, mock_get_db, app, db_test):
    mock_get_db.return_value = db_test

    with app.test_client() as client:
      rv = client.post('/api/v1/schedule',
                       json={
                           'url': 'gemini://foo.server.fake',
                           'every_secs': 60
                       })
      assert '400 BAD REQUEST' == rv.status
      assert {
          'status': 400,
          'message': 'The field `email` is required'
      } == rv.get_json()

  @patch('server.app.get_db')
  def test_create_schedule_missing_url(self, mock_get_db, app, db_test):
    mock_get_db.return_value = db_test

    with app.test_client() as client:
      rv = client.post('/api/v1/schedule',
                       json={
                           'email': 'foo@bar.fake',
                           'every_secs': 60
                       })
      assert '400 BAD REQUEST' == rv.status
      assert {
          'status': 400,
          'message': 'The field `url` is required'
      } == rv.get_json()

  @patch('server.app.get_db')
  def test_create_schedule_missing_every_secs(self, mock_get_db, app, db_test):
    mock_get_db.return_value = db_test

    with app.test_client() as client:
      rv = client.post('/api/v1/schedule',
                       json={
                           'email': 'foo@bar.fake',
                           'url': 'gemini://foo.server.fake',
                       })
      assert '400 BAD REQUEST' == rv.status
      assert {
          'status': 400,
          'message': 'The field `every_secs` is required'
      } == rv.get_json()

  @patch('server.app.get_db')
  def test_create_schedule_every_secs_not_int(self, mock_get_db, app, db_test):
    mock_get_db.return_value = db_test

    with app.test_client() as client:
      rv = client.post('/api/v1/schedule',
                       json={
                           'email': 'foo@bar.fake',
                           'url': 'gemini://foo.server.fake',
                           'every_secs': 'abc',
                       })
      assert '400 BAD REQUEST' == rv.status
      assert {
          'status':
              400,
          'message':
              'The field `every_secs` must be able to be converted to an integer',
      } == rv.get_json()

  @patch('server.app.get_db')
  def test_create_schedule_every_secs_too_small(self, mock_get_db, app,
                                                db_test):
    mock_get_db.return_value = db_test

    with app.test_client() as client:
      rv = client.post('/api/v1/schedule',
                       json={
                           'email': 'foo@bar.fake',
                           'url': 'gemini://foo.server.fake',
                           'every_secs': '-100',
                       })
      assert '400 BAD REQUEST' == rv.status
      assert {
          'status': 400,
          'message': 'The field `every_secs` must be between 60 and 3600',
      } == rv.get_json()

  @patch('server.app.get_db')
  def test_create_schedule_every_secs_too_big(self, mock_get_db, app, db_test):
    mock_get_db.return_value = db_test

    with app.test_client() as client:
      rv = client.post('/api/v1/schedule',
                       json={
                           'email': 'foo@bar.fake',
                           'url': 'gemini://foo.server.fake',
                           'every_secs': '5000',
                       })
      assert '400 BAD REQUEST' == rv.status
      assert {
          'status': 400,
          'message': 'The field `every_secs` must be between 60 and 3600',
      } == rv.get_json()

  @patch('server.app.get_main_db')
  @patch('server.app.flask')
  def test_get_db(self, mock_flask, mock_get_main_db):
    db = get_db()
    assert db is not None
    assert hasattr(mock_flask.g, 'database')

    db_again = get_db()
    assert db_again == db

  @patch('server.app.get_db')
  def test_verify(self, mock_get_db, app, db_test):
    mock_get_db.return_value = db_test

    schedule = Schedule(db_test)
    schedule.insert('foo@bar.bake', 'gemini://foo.fake', 60)

    with app.test_client() as client:
      rv = client.get(f'/api/v1/verify/{schedule.token}')
      assert '200 OK' == rv.status
      assert {'result': True} == rv.get_json()

    with db_test.cursor() as cursor:
      cursor.execute('SELECT verified FROM schedules WHERE id = %s',
                     schedule.id_)
      assert cursor.fetchone()[0]

  @patch('server.app.get_db')
  def test_verify_wrong_token(self, mock_get_db, app, db_test):
    mock_get_db.return_value = db_test

    schedule = Schedule(db_test)
    schedule.insert('foo@bar.bake', 'gemini://foo.fake', 60)

    with app.test_client() as client:
      rv = client.get(f'/api/v1/verify/foobadtoken')
      assert '200 OK' == rv.status
      assert {'result': False} == rv.get_json()

    with db_test.cursor() as cursor:
      cursor.execute('SELECT verified FROM schedules WHERE id = %s',
                     schedule.id_)
      assert not cursor.fetchone()[0]
