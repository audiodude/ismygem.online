from datetime import datetime
import logging
import os
import time

from celery import Celery
import requests
from requests.auth import HTTPBasicAuth

from server.connection import check

redis_url = os.environ.get('REDIS_URL')
mailgun_key = os.environ.get('MAILGUN_KEY')

logger = logging.getLogger(__name__)

app = Celery('periodic_check',
             broker=redis_url,
             backend=redis_url,
             broker_connection_retry_on_startup=True)


@app.task
def check_async(url, email):
  result, message = check(url)
  if not result:
    send_email.delay(url, email, message, time.time())
  return result


@app.task
def send_email(url, email, message, timestamp):
  date_string = datetime.utcfromtimestamp(timestamp).strftime(
      '%a, %b %d %Y at %H:%M:%S (%Y-%m-%d)')
  data = {
      'from': 'checker@ismygem.online',
      'to': email,
      'subject': f'{url} - Gemini check failed',
      'text':
          f'Your Gemini site failed an uptime check on {date_string} UTC.\n\n'
          f'The error message was:\n{message}'
  }

  resp = requests.post('https://api.mailgun.net/v3/ismygem.online/messages',
                       auth=HTTPBasicAuth('api', mailgun_key),
                       data=data)
  if resp.ok:
    return True

  logger.warning('Non ok response from Mailgun:\n' + resp.text)
