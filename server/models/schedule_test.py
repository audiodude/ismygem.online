import uuid

import pytest

from server.db import drop_test_db, get_schema_path, get_test_db
from server.models.schedule import Schedule


@pytest.mark.usefixtures('db_test', autouse=True)
class ScheduleTest:

  @pytest.fixture(autouse=True)
  def db_test(self):
    db = get_test_db()
    with db.cursor() as cursor:
      with open(get_schema_path()) as f:
        cursor.execute(f.read())
    yield db

    # Clean up after
    db.close()
    drop_test_db()
    return

  @pytest.fixture
  def schedule(self, db_test):
    return Schedule(db=db_test)

  def test_insert_email(self, db_test, schedule):
    schedule.insert_schedule('foo@bar.fake', 'gemini://gemini.foo.fake')

    with db_test.cursor() as cursor:
      cursor.execute('SELECT id, email, url, token FROM schedules')
      data = cursor.fetchall()

    assert 1 == len(data)
    s = data[0]
    assert len(s[0]) == 16
    id = uuid.UUID(bytes=s[0])
    assert 'foo@bar.fake' == s[1]
    assert 'gemini://gemini.foo.fake' == s[2]
    assert s[3] is not None
    token = uuid.UUID(s[3])
