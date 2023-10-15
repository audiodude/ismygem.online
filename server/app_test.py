import json
from unittest.mock import patch

import pytest

from server.app import create_app
from server.db import db_test_fixture


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
  def test_create_schedule(self, mock_get_db, app, db_test):
    mock_get_db.return_value = db_test

    with app.test_client() as client:
      rv = client.post('/api/v1/schedule',
                       json={
                           'email': 'foo@bar.fake',
                           'url': 'gemini://foo.server.fake',
                           'every_secs': 60
                       })
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
