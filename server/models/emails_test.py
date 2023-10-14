import pytest

from server.models.base_model_test import BaseModelTest
from server.models.emails import Email


@pytest.mark.usefixtures('db_test', autouse=True)
class EmailsTest(BaseModelTest):

  @pytest.fixture
  def email(self, db_test):
    return Email(db=db_test)

  def test_insert_email(self, db_test, email):
    email.insert_email('foo@bar.fake')

    with db_test.cursor() as cursor:
      cursor.execute('SELECT id, email, token FROM emails')
      data = cursor.fetchall()

    assert 1 == len(data)
    e = data[0]
    assert e[0] is not None
    assert 'foo@bar.fake' == e[1]
    assert e[2] is not None
