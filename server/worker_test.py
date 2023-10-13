import unittest
from unittest.mock import patch, MagicMock

from server.worker import check_async, send_email


class WorkerTest(unittest.TestCase):

  @patch('server.worker.check')
  @patch('server.worker.send_email')
  def test_check_async(self, mock_send_email, mock_check):
    mock_check.return_value = (True, None)
    actual = check_async('gemini://foo.server.fake', 'bar@email.fake')
    self.assertTrue(actual)

  @patch('server.worker.check')
  @patch('server.worker.send_email')
  @patch('server.worker.time.time', return_value=0)
  def test_check_async_false(self, mock_time, mock_send_email, mock_check):
    mock_check.return_value = (False, 'Some message')
    actual = check_async('gemini://foo.server.fake', 'bar@email.fake')

    self.assertFalse(actual)
    mock_send_email.asssert_called_once_with('gemini://foo.server.fake',
                                             'bar@email.fake', 'Some message',
                                             0)

  @patch('server.worker.requests.post')
  def test_send_email(self, mock_requests):
    response = MagicMock()
    response.ok = True
    mock_requests.return_value = response
    actual = send_email('gemini://foo.fake', 'bar@email.fake', 'Some message',
                        474487200)

    self.assertTrue(actual)

    args, kwargs = mock_requests.call_args
    self.assertEqual(1, len(args))
    self.assertEqual('https://api.mailgun.net/v3/ismygem.online/messages',
                     args[0])

    self.assertIsNotNone(kwargs.get('auth'))
    data = kwargs.get('data')
    self.assertIsNotNone(data)
    self.assertEqual('bar@email.fake', data['to'])
    self.assertTrue(data['from'])
    self.assertTrue(data['subject'])
    self.assertTrue(data['text'])
    self.assertIn('Sun, Jan 13 1985', data['text'])
    self.assertIn('1985-01-13', data['text'])
    self.assertIn('18:00:00', data['text'])
