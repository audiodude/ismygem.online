import base64
import hashlib
import os
import uuid

import celery
from redbeat import RedBeatSchedulerEntry
from uuid_extensions import uuid7

salt = os.environ['TOKEN_SALT']


class Schedule:

  def __init__(self, db):
    self.db = db
    self.id_ = uuid7(as_type='bytes')

  @property
  def id_hex(self):
    id_uuid = uuid.UUID(bytes=self.id_)
    return id_uuid.hex

  def insert(self, email, url, every_secs):
    with self.db.cursor() as cursor:
      cursor.execute(
          'INSERT INTO schedules (id, email, url, every_secs)'
          ' VALUES (%s, %s, %s, %s)', (self.id_, email, url, every_secs))

    self.email = email
    self.url = url
    self.every_secs = every_secs
    self.db.commit()

  def load(self, id_=None):
    if id_ is None and self.id_ is None:
      raise RuntimeError('Cannot retrieve data for Schedule with no id_')

    with self.db.cursor() as cursor:
      cursor.execute(
          '''SELECT email, url, every_secs, scheduler_key, first_failure_timestamp
             FROM schedules WHERE id = %s''', self.id_)
      data = cursor.fetchone()
      if data is None:
        raise RuntimeError(f'No data found for Schedule, id={self.id_}')
      self.email, self.url, self.every_secs, self.scheduler_key, self.first_failure_timestamp = data

  def start(self):
    interval = celery.schedules.schedule(run_every=self.every_secs)
    entry = RedBeatSchedulerEntry(f'run-check-{self.token}',
                                  'server.app.worker.check_async',
                                  interval,
                                  args=[self.url, self.email])
    entry.save()
