from unittest.mock import patch
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
    # Creating a UUID from the id will raise exceptions if it's not valid.
    uuid.UUID(bytes=schedule.id_)

  @patch('server.models.schedule.salt', 'pepper')
  def test_create_token(self, schedule):
    token = schedule.create_token('foo@bar.fake', 'gemini://gemini.foo.fake')
    assert schedule.token is not None
    assert 'HFrj5wu0M4QLPDSzRNeBRjohVlw=' == schedule.token

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
