import socket
import unittest
from unittest.mock import patch, MagicMock

from parameterized import parameterized

from server.connection import absolutise_url, check, MAX_REDIRECTS


class ConnnectionTest(unittest.TestCase):
  url = 'gemini://foo.gemini.fake'

  @parameterized.expand(
      (('gemini://server.fake/', '/foo/bar.gmi',
        'gemini://server.fake/foo/bar.gmi'),
       ('gemini://server.fake/foo/baz', 'bar.gmi',
        'gemini://server.fake/foo/bar.gmi'), ('gemini://server.fake', 'foo/bar',
                                              'gemini://server.fake/foo/bar')))
  def test_absolutise_url(self, base, relative, expected):
    actual = absolutise_url(base, relative)
    self.assertEqual(actual, expected)

  @patch('server.connection.socket.create_connection')
  @patch('server.connection.ssl')
  def test_check(self, mock_ssl, mock_socket):
    s = MagicMock()
    context = MagicMock()
    fp = MagicMock()
    s.makefile.return_value = fp
    context.wrap_socket.return_value = s
    mock_ssl.SSLContext.return_value = context
    fp.readline.return_value = b'20 text/gemini'

    actual = check(self.url)
    self.assertEqual((True, None), actual)

  @patch('server.connection.socket.create_connection')
  @patch('server.connection.ssl')
  def test_check_host_not_found(self, mock_ssl, mock_socket):
    s = MagicMock()
    context = MagicMock()
    context.wrap_socket.return_value = s
    mock_ssl.SSLContext.return_value = context
    s.sendall.side_effect = socket.gaierror

    actual = check(self.url)
    self.assertEqual(
        (False, 'Could not find any server at that address (HOST_NOT_FOUND)'),
        actual)

  @patch('server.connection.socket.create_connection')
  @patch('server.connection.ssl')
  def test_check_host_timeout_error(self, mock_ssl, mock_socket):
    s = MagicMock()
    context = MagicMock()
    context.wrap_socket.return_value = s
    mock_ssl.SSLContext.return_value = context
    s.sendall.side_effect = TimeoutError

    actual = check(self.url)
    self.assertEqual(
        (False, 'Could not connect to the site after 30 seconds (TIMEOUT)'),
        actual)

  @patch('server.connection.socket.create_connection')
  @patch('server.connection.ssl')
  def test_check_connection_refused(self, mock_ssl, mock_socket):
    s = MagicMock()
    context = MagicMock()
    context.wrap_socket.return_value = s
    mock_ssl.SSLContext.return_value = context
    s.sendall.side_effect = ConnectionRefusedError

    actual = check(self.url)
    self.assertEqual((False, 'Connection refused by server (CONN_REFUSED)'),
                     actual)

  @patch('server.connection.socket.create_connection')
  @patch('server.connection.ssl')
  def test_check_os_error(self, mock_ssl, mock_socket):
    s = MagicMock()
    context = MagicMock()
    context.wrap_socket.return_value = s
    mock_ssl.SSLContext.return_value = context
    s.sendall.side_effect = OSError

    actual = check(self.url)
    self.assertEqual(
        (False, 'An unknown networking error occurred (NET_UNKNOWN)'), actual)

  @patch('server.connection.socket.create_connection')
  @patch('server.connection.ssl')
  def test_check_follows_redirects(self, mock_ssl, mock_socket):
    s = MagicMock()
    context = MagicMock()
    fp = MagicMock()
    s.makefile.return_value = fp
    context.wrap_socket.return_value = s
    mock_ssl.SSLContext.return_value = context
    fp.readline.side_effect = (b'30 /',) * (MAX_REDIRECTS - 1) + (
        b'20 text/gemini',)

    actual = check(self.url)
    self.assertEqual((True, None), actual)

  @patch('server.connection.socket.create_connection')
  @patch('server.connection.ssl')
  def test_check_max_redirects(self, mock_ssl, mock_socket):
    s = MagicMock()
    context = MagicMock()
    fp = MagicMock()
    s.makefile.return_value = fp
    context.wrap_socket.return_value = s
    mock_ssl.SSLContext.return_value = context
    fp.readline.side_effect = (b'30 /',) * 2 * MAX_REDIRECTS

    actual = check(self.url)
    self.assertEqual((False, 'Too many redirects, > 10 (EXCESS_REDIR)'), actual)

  @patch('server.connection.socket.create_connection')
  @patch('server.connection.ssl')
  def test_check_status_40(self, mock_ssl, mock_socket):
    s = MagicMock()
    context = MagicMock()
    fp = MagicMock()
    s.makefile.return_value = fp
    context.wrap_socket.return_value = s
    mock_ssl.SSLContext.return_value = context
    fp.readline.return_value = b'40 Bad Request'

    actual = check(self.url)
    self.assertEqual((False, 'Error returned from the server (SERVER_ERROR)'),
                     actual)

  @patch('server.connection.socket.create_connection')
  @patch('server.connection.ssl')
  def test_check_status_51(self, mock_ssl, mock_socket):
    s = MagicMock()
    context = MagicMock()
    fp = MagicMock()
    s.makefile.return_value = fp
    context.wrap_socket.return_value = s
    mock_ssl.SSLContext.return_value = context
    fp.readline.return_value = b'51 Not Found'

    actual = check(self.url)
    self.assertEqual((False, 'Error returned from the server (SERVER_ERROR)'),
                     actual)
