import os

import pymysql

creds = {
    'host': os.environ['MYSQL_HOST'],
    'port': int(os.environ['MYSQL_PORT']),
    'user': os.environ['MYSQL_USER'],
}

if os.environ.get('MYSQL_PASSWORD'):
  creds.update(password=os.environ.get('MYSQL_PASSWORD'))

db = pymysql.connect(**creds)
