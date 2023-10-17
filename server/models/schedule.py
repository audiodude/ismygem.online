import base64
import hashlib
import os

import celery
from redbeat import RedBeatSchedulerEntry
from uuid_extensions import uuid7

salt = os.environ['TOKEN_SALT']


class Schedule:

  def __init__(self, db):
    self.db = db
    self.id_ = uuid7(as_type='bytes')

  def create_token(self, email, url):
    word = f'{email}:{salt}:{url}'
    digest = hashlib.sha1(word.encode('utf-8')).digest()
    self.token = base64.b64encode(digest).decode('utf-8')

  def insert(self, email, url, every_secs):
    self.create_token(email, url)
    with self.db.cursor() as cursor:
      cursor.execute(
          'INSERT INTO schedules (id, email, url, token, every_secs)'
          ' VALUES (%s, %s, %s, %s, %s)',
          (self.id_, email, url, self.token, every_secs))
    self.db.commit()

  def verify(self, token):
    with self.db.cursor() as cursor:
      cursor.execute(
          'UPDATE schedules SET verified = 1 WHERE token = %s AND verified = 0',
          token)
      did_verify = cursor.rowcount > 0
      if did_verify:
        cursor.execute('SELECT id FROM schedules WHERE token = %s', token)
        self.id_ = cursor.fetchone()[0]
        self.db.commit()
    return did_verify

  def retrieve(self, id_=None):
    if id_ is None and self.id_ is None:
      raise RuntimeError('Cannot retrieve data for Schedule with no id_')

    with self.db.cursor() as cursor:
      cursor.execute(
          '''SELECT email, url, token, verified, every_secs, last_failure_timestamp
             FROM schedules WHERE id = %s''', self.id_)
      data = cursor.fetchone()
      if data is None:
        raise RuntimeError(f'No data found for Schedule, id={self.id_}')
      self.email, self.url, self.token, self.verified, self.every_secs, self.last_failure_timestamp = data
      self.verified = bool(self.verified)

  def start(self):
    interval = celery.schedules.schedule(run_every=self.every_secs)
    entry = RedBeatSchedulerEntry(f'run-check-{self.token}',
                                  'server.app.worker.check_async',
                                  interval,
                                  args=[self.url, self.email])
    entry.save()
