from uuid_extensions import uuid7

from server.db import get_db


class Email:

  def __init__(self, db=None):
    self.db = db if db else get_db()

  def insert_email(self, address):
    token = uuid7(as_type='str')
    id_ = uuid7(as_type='bytes')
    print(len(id_))
    with self.db.cursor() as cursor:
      cursor.execute(
          'INSERT INTO emails (id, email, token) VALUES (%s, %s, %s)',
          (id_, address, token))
