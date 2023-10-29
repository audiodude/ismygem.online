from datetime import datetime
import logging
import os
import time

from celery import Celery
import requests
from requests.auth import HTTPBasicAuth

from server.connection import check
from server.db import get_db
from server.models.schedule import Schedule

redis_url = os.environ.get('REDIS_URL')
mailgun_key = os.environ.get('MAILGUN_KEY')

logger = logging.getLogger(__name__)

app = Celery('ismygem-online',
             broker=redis_url,
             backend=redis_url,
             redbeat_redis_url=redis_url,
             broker_connection_retry_on_startup=True)


def send_email(data):
  resp = requests.post('https://api.mailgun.net/v3/ismygem.online/messages',
                       auth=HTTPBasicAuth('api', mailgun_key),
                       data=data)
  if resp.ok:
    return True

  logger.warning('Non ok response from Mailgun:\n' + resp.text)


@app.task
def check_async(url, email):
  result, message = check(url)
  if not result:
    send_check_failed_email.delay(url, email, message, time.time())
  return result


@app.task
def send_id_email(db, id_):
  schedule = Schedule(db)
  schedule.id_ = id_
  schedule.load()

  link = f'https://ismygem.online/manage/{schedule.id_hex}'

  data = {
      'from':
          'checker@ismygem.online',
      'to':
          schedule.email,
      'subject':
          f'{schedule.url} - Start your Gemini URL checking',
      'text':
          f'''Thank you for using ismygem.online!

Your site ({schedule.url}) is not yet being checked. Use the link below to start, manage, and delete your uptime checks:

{link}

Be careful: anyone with the link can manage this uptime check (there is no login to this site).

Thanks!
-Travis
''',
  }
  send_email(data)


@app.task
def send_check_failed_email(url, email, message, timestamp):
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
  send_email(data)
