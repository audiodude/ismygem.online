import json
from unittest.mock import patch
import unittest

from server.app import create_app


class AppTest(unittest.TestCase):

  def setUp(self):
    self.app = create_app()
    self.app.config['TESTING'] = True

  @patch('server.app.check')
  def test_check_url(self, mock_check):
    mock_check.return_value = (True, None)
    with self.app.test_client() as client:
      rv = client.post('/api/v1/check',
                       json={'url': 'gemini://foo.server.fake'})
      self.assertEqual({'result': True, 'message': None}, rv.get_json())

  @patch('server.app.check')
  def test_check_url_sends_back_msg(self, mock_check):
    mock_check.return_value = (False,
                               'Some kind of wacky error occured (NET_WACKY)')
    with self.app.test_client() as client:
      rv = client.post('/api/v1/check',
                       json={'url': 'gemini://foo.server.fake'})
      self.assertEqual(
          {
              'result': False,
              'message': 'Some kind of wacky error occured (NET_WACKY)'
          }, rv.get_json())

  @patch('server.app.check')
  def test_check_url_no_json(self, mock_check):
    mock_check.return_value = (True, None)
    with self.app.test_client() as client:
      rv = client.post('/api/v1/check')
      self.assertEqual('415 UNSUPPORTED MEDIA TYPE', rv.status)

  @patch('server.app.check')
  def test_check_url_no_url(self, mock_check):
    mock_check.return_value = (True, None)
    with self.app.test_client() as client:
      rv = client.post('/api/v1/check', json={'foo': 'bar'})
      self.assertEqual('400 BAD REQUEST', rv.status)
