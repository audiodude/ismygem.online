import base64
import hashlib
import os

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
