import uuid

import pytest

from server.db import db_test_fixture
from server.models.schedule import Schedule


@pytest.mark.usefixtures('db_test', autouse=True)
class ScheduleTest:

  @pytest.fixture(autouse=True)
  def db_test(self):
    yield from db_test_fixture()

  @pytest.fixture
  def schedule(self, db_test):
    return Schedule(db=db_test)

  def test_properties(self, schedule):
    assert len(schedule.id_) == 16
    # Creating a UUID from these will raise exceptions if they're not valid.
    id = uuid.UUID(bytes=schedule.id_)
    token = uuid.UUID(schedule.token)

  def test_insert(self, db_test, schedule):
    schedule.insert('foo@bar.fake', 'gemini://gemini.foo.fake', 60)

    with db_test.cursor() as cursor:
      cursor.execute('SELECT id, email, url, token, every_secs FROM schedules')
      data = cursor.fetchall()

    assert 1 == len(data)
    s = data[0]
    assert schedule.id_ == s[0]
    assert 'foo@bar.fake' == s[1]
    assert 'gemini://gemini.foo.fake' == s[2]
    assert schedule.token == s[3]
    assert s[4] == 60
