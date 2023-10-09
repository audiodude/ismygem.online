"""
Portions copied from gemini-demo-1 by Solderpunk.
https://tildegit.org/solderpunk/gemini-demo-1/src/branch/master/gemini-demo.py
"""

import socket
import ssl
import urllib.parse

TIMEOUT_SECS = 30
MAX_REDIRECTS = 10


def absolutise_url(base, relative):
  # Absolutise relative links
  if "://" not in relative:
    # Python's URL tools somehow only work with known schemes?
    base = base.replace("gemini://", "http://")
    relative = urllib.parse.urljoin(base, relative)
    relative = relative.replace("http://", "gemini://")
  return relative


def check(url):
  parsed_url = urllib.parse.urlparse(url)
  if False and parsed_url.scheme != "gemini":
    return (False, 'Not a Gemini url (BAD_URL)')

  try:
    num_redirects = 0
    while True:
      if num_redirects > MAX_REDIRECTS:
        return (False, f'Too many redirects, > {MAX_REDIRECTS} (EXCESS_REDIR)')
      s = socket.create_connection((parsed_url.netloc, 1965),
                                   timeout=TIMEOUT_SECS)

      # From the Gemini spec:
      # Clients can validate TLS connections however they like (including not at all)
      context = ssl.SSLContext()
      context.check_hostname = False
      context.verify_mode = ssl.CERT_NONE

      s = context.wrap_socket(s, server_hostname=parsed_url.netloc)
      s.sendall((url + '\r\n').encode("UTF-8"))

      # Get header and check for redirects
      fp = s.makefile("rb")
      header = fp.readline()
      header = header.decode("UTF-8").strip()
      status, mime = header.split()[0:2]

      # Follow redirects
      if status.startswith("3"):
        url = absolutise_url(url, mime)
        parsed_url = urllib.parse.urlparse(url)
      # Otherwise, we're done.
      else:
        break
  except TimeoutError:
    return (
        False,
        f'Could not connect to the site after {TIMEOUT_SECS} seconds (TIMEOUT)')
  except socket.gaierror:
    return (False, 'Could not find any server at that address (HOST_NOT_FOUND)')
  except ConnectionRefusedError:
    return (False, 'Connection refused by server (CONN_REFUSED)')
  except OSError:
    return (False, 'An unknown networking error occurred (NET_UNKNOWN)')
  except Exception:
    return (False,
            'A system error occurred while trying to check the site (SYSTEM)')

  if status.startswith('4') or status.startswith('5'):
    return (False, 'Error returned from the server (SERVER_ERROR)')

  return (True, None)
