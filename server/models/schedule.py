from uuid_extensions import uuid7

from server.db import get_db


class Schedule:

  def __init__(self, db=None):
    self.db = db if db else get_db()

  def insert_schedule(self, email, url):
    token = uuid7(as_type='str')
    id_ = uuid7(as_type='bytes')
    with self.db.cursor() as cursor:
      cursor.execute(
          'INSERT INTO schedules (id, email, url, token) VALUES (%s, %s, %s, %s)',
          (id_, email, url, token))
