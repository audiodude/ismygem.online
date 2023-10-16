import unittest
from unittest.mock import patch, MagicMock

from server.worker import check_async, send_check_failed_email


class WorkerTest:

  @patch('server.worker.check')
  @patch('server.worker.send_check_failed_email')
  def test_check_async(self, mock_send_email, mock_check):
    mock_check.return_value = (True, None)
    actual = check_async('gemini://foo.server.fake', 'bar@email.fake')
    assert actual

  @patch('server.worker.check')
  @patch('server.worker.send_check_failed_email')
  @patch('server.worker.time.time', return_value=0)
  def test_check_async_false(self, mock_time, mock_send_email, mock_check):
    mock_check.return_value = (False, 'Some message')
    actual = check_async('gemini://foo.server.fake', 'bar@email.fake')

    assert not actual
    mock_send_email.asssert_called_once_with('gemini://foo.server.fake',
                                             'bar@email.fake', 'Some message',
                                             0)

  @patch('server.worker.requests.post')
  def test_send_check_failed_email(self, mock_requests):
    response = MagicMock()
    response.ok = True
    mock_requests.return_value = response
    actual = send_check_failed_email('gemini://foo.fake', 'bar@email.fake',
                                     'Some message', 474487200)

    args, kwargs = mock_requests.call_args
    assert 1 == len(args)
    assert 'https://api.mailgun.net/v3/ismygem.online/messages' == args[0]

    assert kwargs.get('auth') is not None
    data = kwargs.get('data')
    assert data is not None
    assert 'bar@email.fake' == data['to']
    assert data['from']
    assert data['subject']
    assert data['text']
    assert 'Sun, Jan 13 1985' in data['text']
    assert '1985-01-13' in data['text']
    assert '18:00:00' in data['text']
