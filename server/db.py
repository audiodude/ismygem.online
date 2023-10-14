import os

import pymysql
from pymysql.constants import CLIENT


def get_schema_path():
  return os.path.abspath(
      os.path.join(os.path.dirname(__file__), '..', 'db', 'schema.sql'))


def get_db():
  creds = {
      'host': os.environ['MYSQL_HOST'],
      'port': int(os.environ['MYSQL_PORT']),
      'user': os.environ['MYSQL_USER'],
      'database': os.environ['MYSQL_DATABASE']
  }

  if os.environ.get('MYSQL_PASSWORD'):
    creds.update(password=os.environ.get('MYSQL_PASSWORD'))

  return pymysql.connect(**creds)


def get_test_db():
  creds = {
      'host': os.environ['MYSQL_TEST_HOST'],
      'port': int(os.environ['MYSQL_TEST_PORT']),
      'user': os.environ['MYSQL_TEST_USER'],
  }

  if os.environ.get('MYSQL_TEST_PASSWORD'):
    creds.update(password=os.environ.get('MYSQL_TEST_PASSWORD'))

  test_db_name = os.environ['MYSQL_TEST_DATABASE']
  conn = pymysql.connect(**creds, client_flag=CLIENT.MULTI_STATEMENTS)
  with conn.cursor() as cursor:
    retries = 0
    while retries < 2:
      try:
        cursor.execute('CREATE DATABASE `%s`' % test_db_name)
        break
      except pymysql.err.ProgrammingError:
        cursor.execute('DROP DATABASE `%s`' % test_db_name)
        retries += 1

  conn.select_db(test_db_name)
  return conn


def drop_test_db():
  db = get_test_db()
  with db.cursor() as cursor:
    cursor.execute('DROP DATABASE ' + os.environ['MYSQL_TEST_DATABASE'])
  db.close()
