from uuid_extensions import uuid7


class Schedule:

  def __init__(self, db):
    self.db = db

  def insert_schedule(self, email, url, every_secs):
    token = uuid7(as_type='str')
    id_ = uuid7(as_type='bytes')
    with self.db.cursor() as cursor:
      cursor.execute(
          'INSERT INTO schedules (id, email, url, token, every_secs)'
          ' VALUES (%s, %s, %s, %s, %s)', (id_, email, url, token, every_secs))
