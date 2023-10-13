import os

from celery import Celery

from server.connection import check

# DO NOT SUBMIT: Remove the hardcoded URL
redis_url = os.environ.get('REDIS_URL')

app = Celery('periodic_check',
             broker=redis_url,
             backend=redis_url,
             broker_connection_retry_on_startup=True)


@app.task
def check_async(url, email):
  """Returns true if an email was sent, false otherwise."""
  result, message = check(url)
  if not result:
    print(f'Sending email to {email}')
    return True
  return False
