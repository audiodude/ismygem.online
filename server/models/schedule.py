from uuid_extensions import uuid7


class Schedule:

  def __init__(self, db):
    self.db = db
    self.token = uuid7(as_type='str')
    self.id_ = uuid7(as_type='bytes')

  def insert(self, email, url, every_secs):
    with self.db.cursor() as cursor:
      cursor.execute(
          'INSERT INTO schedules (id, email, url, token, every_secs)'
          ' VALUES (%s, %s, %s, %s, %s)',
          (self.id_, email, url, self.token, every_secs))
