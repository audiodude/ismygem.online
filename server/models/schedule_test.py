from datetime import datetime
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

  def test_insert(self, db_test, schedule):
    schedule.insert('foo@bar.fake', 'gemini://gemini.foo.fake', 60)

    with db_test.cursor() as cursor:
      cursor.execute('SELECT id, email, url, every_secs FROM schedules')
      data = cursor.fetchall()

    assert 1 == len(data)
    s = data[0]
    assert schedule.id_ == s[0]
    assert 'foo@bar.fake' == s[1]
    assert 'gemini://gemini.foo.fake' == s[2]
    assert s[3] == 60

  def test_load(self, db_test, schedule):
    schedule.insert('foo@bar.fake', 'gemini://foo.fake', 60)
    expected_id = schedule.id_
    with db_test.cursor() as cursor:
      cursor.execute(
          'UPDATE schedules SET email = "foo2@bar.fake", first_failure_timestamp = "2023-01-01" WHERE id = %s',
          schedule.id_)

    schedule.load()
    assert expected_id == schedule.id_
    assert 'foo2@bar.fake' == schedule.email
    assert 'gemini://foo.fake' == schedule.url
    assert 60 == schedule.every_secs
    assert schedule.scheduler_key is None
    assert datetime(2023, 1, 1) == schedule.first_failure_timestamp
