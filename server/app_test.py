import json
from unittest.mock import patch

import pytest

from server.app import create_app


class AppTest:

  @pytest.fixture
  def app(self):
    app = create_app()
    app.config['TESTING'] = True
    return app

  @patch('server.app.check')
  def test_check_url(self, mock_check, app):
    mock_check.return_value = (True, None)
    with app.test_client() as client:
      rv = client.post('/api/v1/check',
                       json={'url': 'gemini://foo.server.fake'})
      assert {'result': True, 'message': None} == rv.get_json()

  @patch('server.app.check')
  def test_check_url_sends_back_msg(self, mock_check, app):
    mock_check.return_value = (False,
                               'Some kind of wacky error occured (NET_WACKY)')
    with app.test_client() as client:
      rv = client.post('/api/v1/check',
                       json={'url': 'gemini://foo.server.fake'})
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
